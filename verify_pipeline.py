import json
import logging
from pathlib import Path
from app.ingestion.service import IngestionService

# Set up clean terminal logging outputs
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def verify_source_mode(mode: str, count: int = 3):
    logger.info(f"=== Starting Verification for Mode: [{mode.upper()}] ===")
    
    # Configure parameters
    rss_url = "https://www.reddit.com/r/technology/.rss"
    mock_file = Path("data/mock_posts.json")
    
    # Initialize your service orchestrator
    service = IngestionService(rss_url=rss_url, mock_file=mock_file, default_source=mode)
    
    processed_packets = []
    
    # Pull 'count' number of packets through the pipeline
    for i in range(count):
        try:
            packet = service.next_packet()
            processed_packets.append(packet)
            logger.info(f"Successfully processed item {i+1} (ID: {packet['packet_id']})")
        except Exception as e:
            logger.error(f"Failed processing item {i+1}: {e}")
            break

    # Save outputs to local files so you can check them visually
    output_dir = Path("data/output_debug")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"processed_{mode}_output.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.load = json.dump(processed_packets, f, indent=2)
        
    logger.info(f"Saved local debug data to: {output_file}\n")

if __name__ == "__main__":
    # Ensure your raw mock data exists before running mock testing
    mock_path = Path("data/mock_posts.json")
    if not mock_path.exists():
        mock_path.parent.mkdir(exist_ok=True)
        sample_mock = [
            {
                "author": "IsmailTest",
                "title": "<b>Checkout system crashed!</b>",
                "summary": "The payment gateway is throwing a 500 error &amp; loop.",
                "timestamp": "2026-07-16T12:00:00Z"
            }
        ]
        with open(mock_path, "w", encoding="utf-8") as f:
            json.dump(sample_mock, f, indent=2)

    # Execute checks on both pipeline components
    verify_source_mode("mock", count=1)
    verify_source_mode("rss", count=3)