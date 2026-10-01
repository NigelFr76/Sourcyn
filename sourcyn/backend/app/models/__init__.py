from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ProcurementRequest(Base):
    __tablename__ = "procurement_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String)
    quantity = Column(Integer)
    budget = Column(Float)
    currency = Column(String, default="INR")
    max_delivery_days = Column(Integer)
    natural_language_request = Column(String)
    status = Column(String, default="DRAFT") # DRAFT, ANALYZING, ANALYSIS_COMPLETE, PENDING_APPROVAL, APPROVED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Structured requirements extracted by agent
    structured_requirements = Column(JSON, nullable=True)

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    is_internal = Column(Boolean, default=True) # True if historical internal vendor, False if found via web
    certifications = Column(JSON) # List of certifications
    capacity = Column(String)

class VendorPerformance(Base):
    __tablename__ = "vendor_performance"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    total_orders = Column(Integer, default=0)
    on_time_delivery_rate = Column(Float, default=1.0)
    average_delay_days = Column(Float, default=0.0)
    rejected_shipments = Column(Integer, default=0)
    rating = Column(Float, default=5.0)

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    procurement_request_id = Column(Integer, ForeignKey("procurement_requests.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    total_amount = Column(Float)
    currency = Column(String, default="INR")
    delivery_days = Column(Integer)
    warranty_months = Column(Integer)
    status = Column(String) # EXTRACTED, VALIDATED, MALFORMED
    extracted_data = Column(JSON) # Full raw extraction
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class WebResearchResult(Base):
    __tablename__ = "web_research_results"

    id = Column(Integer, primary_key=True, index=True)
    procurement_request_id = Column(Integer, ForeignKey("procurement_requests.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    search_query = Column(String)
    url = Column(String)
    title = Column(String)
    source_type = Column(String) # Vendor Website, Retailer, Public Database, etc.
    extracted_information = Column(JSON)
    retrieved_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="SUCCESS") # SUCCESS, FAILED

class ComplianceResult(Base):
    __tablename__ = "compliance_results"

    id = Column(Integer, primary_key=True, index=True)
    procurement_request_id = Column(Integer, ForeignKey("procurement_requests.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    compliance_score = Column(Float) # Percentage 0-100
    details = Column(JSON) # {"Processor": "PASS", "RAM": "PASS"}

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    procurement_request_id = Column(Integer, ForeignKey("procurement_requests.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    risk_level = Column(String) # LOW, MEDIUM, HIGH, INSUFFICIENT_DATA
    factors = Column(JSON)
    evidence = Column(JSON)
    mitigation = Column(JSON)

class ProcurementScore(Base):
    __tablename__ = "procurement_scores"

    id = Column(Integer, primary_key=True, index=True)
    procurement_request_id = Column(Integer, ForeignKey("procurement_requests.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    price_score = Column(Float)
    compliance_score = Column(Float)
    delivery_score = Column(Float)
    reliability_score = Column(Float)
    risk_score = Column(Float)
    overall_score = Column(Float)

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True)
    procurement_request_id = Column(Integer, ForeignKey("procurement_requests.id"))
    agent_name = Column(String)
    status = Column(String) # PENDING, RUNNING, COMPLETED, FAILED
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    input_summary = Column(JSON, nullable=True)
    output = Column(JSON, nullable=True)
    error = Column(String, nullable=True)

class ProcurementDecision(Base):
    __tablename__ = "procurement_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    procurement_request_id = Column(Integer, ForeignKey("procurement_requests.id"))
    recommended_vendor_id = Column(Integer, ForeignKey("vendors.id"))
    explanation = Column(String)
    trade_offs = Column(JSON)
    status = Column(String, default="PENDING_APPROVAL") # PENDING_APPROVAL, APPROVED, REJECTED

class ApprovalHistory(Base):
    __tablename__ = "approval_history"
    
    id = Column(Integer, primary_key=True, index=True)
    procurement_decision_id = Column(Integer, ForeignKey("procurement_decisions.id"))
    action = Column(String) # APPROVED, REJECTED, REQUEST_REANALYSIS
    timestamp = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
