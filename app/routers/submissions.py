from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime

from app.database import get_database
from app.models import FormSubmission

router = APIRouter(tags=["submissions"])


@router.get("/submissions", response_model=List[dict])
async def get_submissions(
    mission: Optional[str] = Query(None, description="Filter by mission type"),
    limit: int = Query(50, ge=1, le=100, description="Number of submissions to return"),
    skip: int = Query(0, ge=0, description="Number of submissions to skip"),
):
    """
    Retrieve form submissions from the database.
    
    - **mission**: Optional filter by mission type (contact, donation, volunteer, information)
    - **limit**: Maximum number of results (1-100)
    - **skip**: Number of results to skip (for pagination)
    """
    db = get_database()
    
    # Build query filter
    query_filter = {}
    if mission:
        query_filter["mission"] = mission
    
    # Fetch submissions
    cursor = db.submissions.find(query_filter).sort("submitted_at", -1).skip(skip).limit(limit)
    submissions = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string for JSON serialization
    for submission in submissions:
        submission["_id"] = str(submission["_id"])
    
    return submissions


@router.get("/submissions/stats")
async def get_submission_stats():
    """
    Get statistics about form submissions.
    
    Returns counts by mission type and total submissions.
    """
    db = get_database()
    
    # Total count
    total = await db.submissions.count_documents({})
    
    # Count by mission
    pipeline = [
        {
            "$group": {
                "_id": "$mission",
                "count": {"$sum": 1}
            }
        }
    ]
    
    mission_counts = {}
    async for doc in db.submissions.aggregate(pipeline):
        mission_counts[doc["_id"]] = doc["count"]
    
    return {
        "total_submissions": total,
        "by_mission": mission_counts,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.delete("/submissions/{submission_id}")
async def delete_submission(submission_id: str):
    """
    Delete a specific submission by ID.
    
    - **submission_id**: MongoDB ObjectId of the submission to delete
    """
    from bson import ObjectId
    from bson.errors import InvalidId
    
    db = get_database()
    
    try:
        object_id = ObjectId(submission_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid submission ID format")
    
    result = await db.submissions.delete_one({"_id": object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return {"message": "Submission deleted successfully", "id": submission_id}
