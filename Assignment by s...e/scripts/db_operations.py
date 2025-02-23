from sqlalchemy.orm import Session
from scripts.db_models import LogTable
from typing import List, Dict

def create_job_log(db: Session, reference_number: int, product_names: List[str], image_count: int, status: str):
    product_names = ",".join(product_names)  
    db_job_log = LogTable(reference_number=reference_number, product_names=product_names, image_count=image_count, status=status)
    db.add(db_job_log)
    db.commit()
    db.refresh(db_job_log)
    return db_job_log

def delete_job_log(db: Session, reference_number: int):
    db_job_log = db.query(LogTable).filter(LogTable.reference_number == reference_number).first()
    if db_job_log:
        db.delete(db_job_log)
        db.commit()
    return db_job_log

def update_status_by_reference(db: Session, reference_number: int, new_status: str):
    db_job_log = db.query(LogTable).filter(LogTable.reference_number == reference_number).first()
    if db_job_log:
        db_job_log.status = new_status
        db.commit()
        db.refresh(db_job_log)
        return db_job_log
    return None

def get_complete_rows_by_reference(db: Session, reference_number: int):
    return db.query(LogTable).filter(LogTable.reference_number == reference_number, LogTable.status == 'completed').all()

def update_product_names_by_reference(db: Session, reference_number: int, new_product_names: List[str]):
    product_names = ",".join(new_product_names)  # Join product names into a comma-separated string
    db_job_log = db.query(LogTable).filter(LogTable.reference_number == reference_number).first()
    if db_job_log:
        db_job_log.product_names = product_names
        db.commit()
        db.refresh(db_job_log)
        return db_job_log
    return None

def get_status_by_reference(db: Session, reference_number: int):
    db_job_log = db.query(LogTable).filter(LogTable.reference_number == reference_number).first()
    if db_job_log:
        return db_job_log.status
    return None 

def is_reference_present(db: Session, reference_number: int) -> bool:
    return db.query(LogTable).filter(LogTable.reference_number == reference_number).first() is not None

def get_total_rows(db: Session) -> int:
    return db.query(LogTable).count()