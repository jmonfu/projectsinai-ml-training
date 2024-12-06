#!/usr/bin/env python
"""
Data preparation script for SmartSynch task categorization.
This script processes the raw training data and prepares it for model training.
"""

import argparse
import logging
from pathlib import Path
import numpy as np
from smartsynch.data.processor import DataProcessor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main data preparation pipeline."""
    parser = argparse.ArgumentParser(description='Prepare data for model training')
    parser.add_argument(
        '--input', 
        type=str, 
        default='data/training_data.json',
        help='Path to input training data'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        default='data/processed',
        help='Directory to save processed data'
    )
    parser.add_argument(
        '--test-size', 
        type=float, 
        default=0.2,
        help='Proportion of data to use for validation'
    )
    args = parser.parse_args()

    try:
        # Initialize processor
        logger.info("Initializing data processor...")
        processor = DataProcessor()

        # Prepare data
        logger.info(f"Processing data from {args.input}...")
        embeddings, labels = processor.prepare_data(args.input)
        logger.info(f"Generated {len(embeddings)} embeddings with shape {embeddings.shape}")

        # Split data
        logger.info(f"Splitting data with test size {args.test_size}...")
        splits = processor.split_data(embeddings, labels, test_size=args.test_size)
        X_train, X_val, y_train, y_val = splits

        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save processed data
        logger.info(f"Saving processed data to {output_dir}...")
        np.save(output_dir / "X_train.npy", X_train)
        np.save(output_dir / "X_val.npy", X_val)
        np.save(output_dir / "y_train.npy", y_train)
        np.save(output_dir / "y_val.npy", y_val)

        # Save category mapping
        np.save(output_dir / "category_map.npy", processor.category_map)

        logger.info("Data preparation completed successfully!")

    except Exception as e:
        logger.error(f"Error during data preparation: {str(e)}")
        raise

if __name__ == "__main__":
    main()
