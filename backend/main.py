from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
from datetime import datetime
import os

# Import your existing analyzer
try:
    from analyzers.analyzer import analyze_transcript
    from utils.detectors import pre_check_callback, pre_check_interaction, pre_check_time_respect, pre_check_needs, pre_check_transfer
    print("✅ Successfully imported analyzer functions")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("⚠️  Using mock analyzer for demo")
    
    # Define mock functions only if import fails
    def analyze_transcript(transcript, model="gpt-4o"):
        # Mock analysis for demo
        print("🔧 Using MOCK analyzer - this is demo data")
        return {
            'overall_scores': {
                'total_score': 35,
                'max_possible_score': 45,
                'percentage_score': 77.8
            },
            'first_response_analysis': {
                'score': 5,
                'reasoning': 'Agent responded within 2 minutes and requested callback.',
                'response_time_seconds': 89
            },
            'security_verification_analysis': {
                'score': 8,
                'reasoning': 'Agent asked for 3 security elements and customer provided all.'
            },
            'customer_needs_analysis': {
                'score': 4,
                'reasoning': 'Agent identified the reason and restated with confirmation.'
            },
            'interaction_analysis': {
                'score': 4,
                'reasoning': 'Proper language used and responsibility accepted.'
            },
            'time_respect_analysis': {
                'score': 7,
                'reasoning': 'Regular check-ins maintained throughout the conversation.'
            },
            'needs_identification_analysis': {
                'score': 3,
                'reasoning': 'Minimal redundant questions asked.'
            },
            'transfer_analysis': {
                'score': 8,
                'reasoning': 'Voice services question was properly asked.'
            }
        }
    
    # Mock detector functions
    def pre_check_callback(transcript):
        return True
    
    def pre_check_interaction(transcript):
        return True
    
    def pre_check_time_respect(transcript):
        return True
    
    def pre_check_needs(transcript):
        return True
    
    def pre_check_transfer(transcript):
        return True

app = FastAPI(title="QA Chat Analyzer API", version="1.0.0")

# CORS middleware - include all possible frontend ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:5173", 
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def init_db():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect('data/qa_analyses.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transcript_text TEXT,
            model_used TEXT,
            overall_score INTEGER,
            max_score INTEGER,
            percentage_score REAL,
            analysis_results TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

init_db()

class AnalysisRequest(BaseModel):
    transcript: str
    model: str = "gpt-4o"

@app.get("/")
async def root():
    return {
        "message": "QA Chat Analyzer API", 
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "/api/analyze",
            "analyses": "/api/analyses",
            "dashboard_stats": "/api/dashboard/stats",
            "docs": "/docs"
        }
    }

@app.post("/api/analyze")
async def analyze_chat(request: AnalysisRequest):
    try:
        print(f"📨 Received analysis request")
        print(f"   Transcript length: {len(request.transcript)} characters")
        print(f"   Model: {request.model}")
        
        # Perform analysis using your existing function
        result = analyze_transcript(request.transcript, model=request.model)
        
        print(f"✅ Analysis completed")
        print(f"   Overall score: {result.get('overall_scores', {}).get('total_score', 0)}/{result.get('overall_scores', {}).get('max_possible_score', 45)}")
        print(f"   Percentage: {result.get('overall_scores', {}).get('percentage_score', 0)}%")
        
        # Store in database
        conn = sqlite3.connect('data/qa_analyses.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO analyses 
            (transcript_text, model_used, overall_score, max_score, percentage_score, analysis_results)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            request.transcript,
            request.model,
            result.get('overall_scores', {}).get('total_score', 0),
            result.get('overall_scores', {}).get('max_possible_score', 45),
            result.get('overall_scores', {}).get('percentage_score', 0),
            json.dumps(result)
        ))
        conn.commit()
        analysis_id = cursor.lastrowid
        conn.close()
        
        print(f"💾 Analysis saved to database with ID: {analysis_id}")
        
        return {
            "analysis_id": analysis_id,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/api/analyses")
async def get_analyses(limit: int = 50, offset: int = 0):
    conn = sqlite3.connect('data/qa_analyses.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, transcript_text, model_used, overall_score, max_score, 
               percentage_score, created_at 
        FROM analyses 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
    ''', (limit, offset))
    
    analyses = []
    for row in cursor.fetchall():
        analyses.append({
            "id": row[0],
            "transcript_preview": row[1][:100] + "..." if len(row[1]) > 100 else row[1],
            "model_used": row[2],
            "overall_score": row[3],
            "max_score": row[4],
            "percentage_score": row[5],
            "created_at": row[6]
        })
    
    conn.close()
    return {"analyses": analyses}

@app.get("/api/analyses/{analysis_id}")
async def get_analysis_detail(analysis_id: int):
    conn = sqlite3.connect('data/qa_analyses.db')
    cursor = conn.cursor()
    cursor.execute('SELECT analysis_results FROM analyses WHERE id = ?', (analysis_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return json.loads(row[0])

@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    conn = sqlite3.connect('data/qa_analyses.db')
    cursor = conn.cursor()
    
    try:
        # Total analyses
        cursor.execute('SELECT COUNT(*) FROM analyses')
        total_analyses = cursor.fetchone()[0] or 0
        
        # Average score
        cursor.execute('SELECT AVG(percentage_score) FROM analyses')
        avg_score_result = cursor.fetchone()[0]
        avg_score = float(avg_score_result) if avg_score_result else 0.0
        
        # Recent analyses (last 7 days)
        cursor.execute('''
            SELECT COUNT(*) FROM analyses 
            WHERE created_at >= datetime('now', '-7 days')
        ''')
        recent_analyses = cursor.fetchone()[0] or 0
        
        # Score distribution
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN percentage_score >= 80 THEN 1 ELSE 0 END) as excellent,
                SUM(CASE WHEN percentage_score >= 60 AND percentage_score < 80 THEN 1 ELSE 0 END) as good,
                SUM(CASE WHEN percentage_score >= 40 AND percentage_score < 60 THEN 1 ELSE 0 END) as average,
                SUM(CASE WHEN percentage_score < 40 THEN 1 ELSE 0 END) as poor
            FROM analyses
        ''')
        dist = cursor.fetchone()
        score_distribution = {
            "excellent": dist[0] or 0,
            "good": dist[1] or 0,
            "average": dist[2] or 0,
            "poor": dist[3] or 0
        }
        
        print(f"📊 Dashboard stats: {total_analyses} total analyses, avg score: {avg_score}%")
        
        return {
            "total_analyses": total_analyses,
            "average_score": round(avg_score, 2),
            "recent_analyses": recent_analyses,
            "score_distribution": score_distribution
        }
        
    except Exception as e:
        print(f"❌ Error getting dashboard stats: {e}")
        # Return default stats if table is empty or error occurs
        return {
            "total_analyses": 0,
            "average_score": 0,
            "recent_analyses": 0,
            "score_distribution": {
                "excellent": 0,
                "good": 0,
                "average": 0,
                "poor": 0
            }
        }
    finally:
        conn.close()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🚀 QA Chat Analyzer API Starting...")
    print("="*50)
    print("📊 Endpoints:")
    print("   • API: http://localhost:8000")
    print("   • Docs: http://localhost:8000/docs")
    print("   • Health: http://localhost:8000/health")
    print("="*50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")