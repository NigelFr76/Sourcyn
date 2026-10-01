from datetime import datetime, timedelta
import json
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import (
    Vendor, VendorPerformance, ProcurementRequest, Quotation, 
    WebResearchResult, ComplianceResult, RiskAssessment, ProcurementScore, ProcurementDecision
)

def seed_data(db: Session):
    Base.metadata.create_all(bind=engine)
    
    if db.query(Vendor).first():
        print("Database already seeded!")
        return

    # Seed 10 Vendors
    vendors = [
        Vendor(name="TechSolutions Global", location="Bangalore, India", is_internal=True, certifications=["ISO 9001", "ISO 27001"], capacity="10000 units/month"),
        Vendor(name="Nexus Electronics", location="Shenzhen, China", is_internal=True, certifications=["ISO 9001"], capacity="50000 units/month"),
        Vendor(name="Alpha Hardware Inc", location="Austin, TX", is_internal=True, certifications=["ISO 9001", "GreenTech Certified"], capacity="5000 units/month"),
        Vendor(name="Reliable IT Suppliers", location="Mumbai, India", is_internal=True, certifications=[], capacity="2000 units/month"),
        Vendor(name="Quantum Computing Devices", location="Taipei, Taiwan", is_internal=True, certifications=["ISO 27001", "RoHS"], capacity="15000 units/month"),
        Vendor(name="Global Tech Distributors", location="London, UK", is_internal=False, certifications=["ISO 9001"], capacity="Unknown"),
        Vendor(name="Prime Equipments", location="Delhi, India", is_internal=True, certifications=["ISO 9001"], capacity="8000 units/month"),
        Vendor(name="DataSystems Corp", location="Singapore", is_internal=True, certifications=["ISO 27001", "SOC2"], capacity="12000 units/month"),
        Vendor(name="Budget Laptops Ltd", location="Pune, India", is_internal=False, certifications=[], capacity="Unknown"),
        Vendor(name="SecureTech Partners", location="Frankfurt, Germany", is_internal=True, certifications=["ISO 9001", "ISO 27001", "GDPR Compliant"], capacity="10000 units/month"),
    ]
    db.add_all(vendors)
    db.commit()

    # Seed Vendor Performance
    performances = [
        VendorPerformance(vendor_id=1, total_orders=45, on_time_delivery_rate=0.92, average_delay_days=1.5, rejected_shipments=1, rating=4.5),
        VendorPerformance(vendor_id=2, total_orders=120, on_time_delivery_rate=0.98, average_delay_days=0.2, rejected_shipments=3, rating=4.8),
        VendorPerformance(vendor_id=3, total_orders=12, on_time_delivery_rate=0.85, average_delay_days=3.0, rejected_shipments=0, rating=4.1),
        VendorPerformance(vendor_id=4, total_orders=80, on_time_delivery_rate=0.75, average_delay_days=5.5, rejected_shipments=5, rating=3.2),
        VendorPerformance(vendor_id=5, total_orders=200, on_time_delivery_rate=0.95, average_delay_days=1.0, rejected_shipments=2, rating=4.6),
        VendorPerformance(vendor_id=7, total_orders=30, on_time_delivery_rate=0.88, average_delay_days=2.5, rejected_shipments=1, rating=4.0),
        VendorPerformance(vendor_id=8, total_orders=65, on_time_delivery_rate=0.99, average_delay_days=0.1, rejected_shipments=0, rating=4.9),
        VendorPerformance(vendor_id=10, total_orders=22, on_time_delivery_rate=0.96, average_delay_days=0.5, rejected_shipments=0, rating=4.7),
    ]
    db.add_all(performances)
    db.commit()

    # Seed 1 Procurement Request
    req = ProcurementRequest(
        title="Annual Laptop Refresh 2026",
        category="Business Laptop",
        quantity=500,
        budget=5000000,
        currency="INR",
        max_delivery_days=30,
        natural_language_request="We need 500 business laptops. Intel i7 or equivalent. 16GB RAM. 512GB SSD. 3-year warranty. Delivery within 30 days. Budget ₹50 lakh.",
        status="DRAFT",
        structured_requirements={
            "product_category": "Business Laptop",
            "quantity": 500,
            "requirements": [
                {"criterion": "Processor", "requirement": "Intel i7 or equivalent", "mandatory": True},
                {"criterion": "RAM", "requirement": "16GB", "mandatory": True},
                {"criterion": "Storage", "requirement": "512GB SSD", "mandatory": True},
                {"criterion": "Warranty", "requirement": "3-year warranty", "mandatory": True}
            ],
            "budget": 5000000,
            "currency": "INR",
            "max_delivery_days": 30
        }
    )
    db.add(req)
    db.commit()

    print("Seed data successfully inserted!")

if __name__ == "__main__":
    db = SessionLocal()
    seed_data(db)
    db.close()
