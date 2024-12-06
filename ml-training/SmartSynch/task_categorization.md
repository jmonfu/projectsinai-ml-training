# Smart Task Categorization - Implementation Plan
## Overview
This document outlines the implementation strategy for training and deploying a TensorFlow.js model for automatic task categorization in SmartSynch.

## Project Structure

smartsynch/
├── data/
│ ├── training_data.json     # Initial training dataset
│ └── user_data.json        # Structure for collecting user data
├── models/
│ ├── base_model/          # Pre-trained Sentence Transformer
│ └── fine_tuned/         # Storage for fine-tuned models
├── smartsynch/           # Main package directory
│ ├── __init__.py        # Makes smartsynch a Python package
│ ├── data/
│ │ ├── __init__.py
│ │ └── processor.py     # Data processing utilities
│ ├── models/
│ │ ├── __init__.py
│ │ ├── predictor.py    # Prediction interface
│ │ └── manager.py      # Model loading and handling
│ └── utils/
│   ├── __init__.py
│   └── helpers.py      # Common utility functions
├── scripts/
│ ├── prepare_data.py    # Data preprocessing script
│ ├── train_model.py     # Model training script
│ └── evaluate_model.py  # Model evaluation script
├── tests/              # Unit tests directory
│ ├── __init__.py
│ ├── test_processor.py
│ └── test_predictor.py
├── README.md           # Project documentation
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
├── setup.py           # Package installation script
└── .gitignore        # Git ignore file

## Implementation Steps

### 1. Data Collection & Preparation
#### Initial Training Data (data/training_data.json)
- Create a comprehensive dataset of task titles and descriptions mapped to categories
- Include various examples for each existing category:
  - Development (e.g., "Implement user authentication", "Fix API endpoint bug")
  - Design (e.g., "Create landing page mockup", "Design new logo")
  - Research (e.g., "Investigate performance issues", "Research competitor features")
  - Meeting (e.g., "Weekly team sync", "Client presentation")
  - Planning (e.g., "Sprint planning", "Roadmap review")

#### Data Structure
```json
{
  "samples": [
    {
      "title": "string",
      "description": "string",
      "category": "string"
    }
  ]
}
```

### 2. Model Architecture
#### Base Model
- Use Sentence-Transformers (BERT-based) for text embedding
- Benefits:
  - Pre-trained on large-scale data
  - State-of-the-art text understanding
  - Easy integration with PyTorch/TensorFlow
  - Optimized for production deployment

#### Classification Layer
- Add a custom classification head using PyTorch or TensorFlow
- Architecture:
  - Dense layer (128 units, ReLU activation)
  - Dropout layer (0.2)
  - Output layer (softmax activation)

### 3. Training Pipeline
1. **Data Preprocessing**
   - Text cleaning and normalization using NLTK/spaCy
   - Tokenization using transformers
   - Embedding generation using Sentence-Transformers
   - Training/validation split using scikit-learn

2. **Model Training**
   - Initial training using PyTorch/TensorFlow
   - Fine-tuning capabilities with custom data
   - Early stopping and model checkpointing
   - Experiment tracking with MLflow or Weights & Biases

3. **Model Evaluation**
   - Accuracy metrics
   - Confusion matrix
   - Cross-validation

### 4. Web Integration
#### Model Serving
- Deploy model using FastAPI or Flask
- REST API endpoints for predictions
- Model versioning and A/B testing
- Caching with Redis

#### Inference Pipeline
1. API endpoint for real-time predictions
2. Batch prediction capabilities
3. Confidence threshold handling
4. Category suggestion logic

### 5. Continuous Learning
#### User Feedback Collection
- Store accepted/rejected predictions
- Track manual category assignments
- Confidence scoring system

#### Model Updates
- Periodic model fine-tuning with user data
- Version control for model updates
- A/B testing framework for improvements

## Integration with Frontend
### Changes Required
1. Add API client for model predictions
2. Implement prediction caching
3. Add UI elements for category suggestions
4. Handle new category creation flow

### User Experience Flow
1. User types task title/description
2. Model predicts category in real-time
3. If confidence > threshold:
   - Auto-select category
   - Show visual indicator
4. If confidence < threshold:
   - Show suggested categories
   - Option to create new category

## Performance Considerations
- Model quantization for faster inference
- API response time optimization
- Caching strategy
- Horizontal scaling capabilities

## Next Steps
1. Set up Python development environment
2. Create initial training dataset
3. Implement data preprocessing pipeline
4. Train base model using PyTorch/TensorFlow
5. Deploy model API
6. Implement frontend integration
7. Add continuous learning capabilities

## Implementation Progress

### Completed Steps:
1. ✓ Set up Python development environment
   - Installed required packages
   - Created project structure
   - Set up setup.py with dependencies
   Files:
   - setup.py: Package configuration and dependencies
   - requirements.txt: Production dependencies
   - requirements-dev.txt: Development dependencies

2. ✓ Create initial training dataset
   - Created training_data.json with 100 examples
   - 20 examples per category
   - Followed defined data structure
   Files:
   - data/training_data.json: Training dataset
   - data/user_data.json: Structure for user feedback

3. ✓ Implement data preprocessing pipeline
   - Created DataProcessor class with text cleaning and embedding generation
   - Implemented unit tests for all processor functionality
   - Created prepare_data.py script for data preparation
   - Added logging and error handling
   Files:
   - smartsynch/data/embeddings.py: Text embedding generation
     - Uses sentence-transformers for generating embeddings
     - Handles batching and caching of embeddings
     - Provides interface for embedding text data

   - smartsynch/data/cleaning.py: Text preprocessing utilities
     - Removes special characters and formatting
     - Handles HTML tags and markdown
     - Normalizes whitespace and casing
     - Language detection and filtering

   - smartsynch/data/augmentation.py: Data augmentation tools
     - Synonym replacement
     - Back translation
     - Random insertion/deletion
     - Generates additional training examples

   - smartsynch/data/validation.py: Data validation utilities
     - Validates input data format and structure
     - Checks for required fields
     - Validates category labels
     - Ensures data quality standards

   - smartsynch/data/sampling.py: Dataset sampling utilities
     - Handles class imbalance
     - Implements various sampling strategies
     - Creates train/val/test splits
     - Generates balanced mini-batches

   - smartsynch/data/loader.py: Data loading utilities
     - Loads data from various formats (JSON, CSV, etc)
     - Handles streaming of large datasets
     - Implements data iterators and batching
     - Manages data versioning

   - smartsynch/data/processor.py: Core data processing logic
     - Implements DataProcessor class
     - Handles text cleaning and normalization
     - Manages embedding generation pipeline
     - Coordinates data validation and augmentation
     - Provides unified processing interface
   
   - scripts/prepare_data.py: Data preparation script
     - Loads raw training data
     - Applies preprocessing pipeline
     - Generates and saves embeddings
     - Creates train/val/test splits
     - Outputs processed datasets
   
   - tests/test_processor.py: Unit tests for processor
     - Tests DataProcessor functionality
     - Validates preprocessing steps
     - Checks embedding generation
     - Verifies data splits
     - Ensures data quality

4. ✓ Train base model using PyTorch/TensorFlow
   - Implemented model architecture using PyTorch/TensorFlow
   - Implemented unit tests for model
   - Created train_model.py script for model training
   - Added logging and error handling
   Files:
   - smartsynch/models/training/: Training utilities
     - Loss functions and optimizers
     - Training loop implementation 
     - Checkpointing and early stopping
     - Learning rate scheduling
   - smartsynch/models/evaluation/: Evaluation utilities
     - Metrics calculation
     - Model comparison
     - Performance analysis
     - Cross-validation
   - smartsynch/models/classifier.py: Model architecture definition (✓)
     - Sentence-Transformer embedding layer
     - Classification head (Dense->Dropout->Softmax)
     - Model configuration and hyperparameters
     - Attention mechanism for text focus
     - Multi-head attention layers
     - Positional encoding for sequence order
     - Layer normalization and residual connections
     - Regularization techniques (L1/L2, dropout)
     - Custom loss functions for imbalanced data
     - Gradient clipping for stability
   - smartsynch/models/predictor.py: Prediction interface (✓)
     - Model inference pipeline
     - Batch prediction handling
     - Confidence scoring
     - Category mapping
     - Input validation
     - Error handling
     - Caching integration
     - Performance optimization
   - smartsynch/models/manager.py: Model loading and saving (✓) 
     - Model versioning
     - Checkpoint management
     - Model registry
     - A/B test variants
     - Model metadata
     - Storage backends
     - Cleanup policies
   - tests/test_predictor.py: Predictor unit tests (✓)
     - Inference tests
     - Batch processing tests
     - Error handling tests
     - Performance tests
     - Integration tests
   - tests/test_classifier.py: Model unit tests (✓)
     - Architecture tests
     - Training tests
     - Evaluation tests
     - Serialization tests
   - scripts/train_model.py: Training script (✓)
     - Training loop
     - Validation loop
     - Hyperparameter handling
     - Experiment tracking
     - Model export
   - configs/training_config.yaml: Training hyperparameters (✓)
     - Model architecture
     - Training settings
     - Optimizer config
     - Data pipeline
     - Logging config
   - smartsynch/utils/metrics.py: Training metrics and logging (✓)
     - Custom metrics
     - Progress tracking
     - Performance logging
     - Visualization utils
     - Export functions

5. ✓ Deploy model API
   - Implemented API endpoints for predictions
   - Implemented API client for model predictions
   - Implemented API versioning and A/B testing
   - Implemented API caching with Redis
   Files:
   - smartsynch/api/: FastAPI application
   - smartsynch/api/routes/: API endpoints
   - docker/: Containerization files

6. ✓ Evaluation Pipeline (Completed) ✓
Files Created:
- scripts/evaluate_model.py: Evaluation script (✓)
  - Model evaluation loop
  - Metric calculation
  - Results visualization
  - Report generation
  - Cross-validation
  - Error analysis
- smartsynch/utils/evaluation.py: Evaluation metrics (✓)
  - Accuracy metrics
  - Precision/Recall
  - F1 score
  - Confusion matrix
  - ROC curves
  - Custom metrics
- tests/test_evaluation.py: Metric unit tests (✓)
  - Metric calculation tests
  - Edge case handling
  - Integration tests
  - Visualization tests
  - Report generation tests

### Current Status:
- Model architecture implemented and tested
- Training pipeline completed with configuration
- Evaluation pipeline implemented with metrics
- Ready to proceed with web integration

### Next Steps:
1. Implement frontend integration
2. Add continuous learning capabilities

## Implementation Tracking

### 1. Environment Setup ✓
Files Created:
- setup.py: Package dependencies and configuration
- requirements.txt: Production dependencies
- requirements-dev.txt: Development dependencies
- .gitignore: Git ignore patterns

### 2. Initial Dataset Creation ✓
Files Created:
- data/training_data.json: 100 training examples (20 per category)
- data/user_data.json: Structure for user feedback collection

### 3. Data Preprocessing Pipeline ✓
Files Created:
- smartsynch/data/processor.py: DataProcessor class implementation
- scripts/prepare_data.py: Data preparation script
- tests/test_processor.py: Unit tests for processor
- smartsynch/data/__init__.py: Package initialization

### 4. Model Architecture (Completed) ✓
Files Created:
- smartsynch/models/classifier.py: Model architecture definition (✓)
  - Sentence-Transformer embedding layer
  - Classification head (Dense->Dropout->Softmax)
- smartsynch/models/predictor.py: Prediction interface (✓)
- smartsynch/models/manager.py: Model loading and saving (✓)
- tests/test_predictor.py: Predictor unit tests (✓)
- tests/test_classifier.py: Model unit tests (✓)

### 5. Training Pipeline (Completed) ✓
Files Created:
- scripts/train_model.py: Training script (✓)
- configs/training_config.yaml: Training hyperparameters (✓)
- smartsynch/utils/metrics.py: Training metrics and logging (✓)

### 6. Evaluation Pipeline (Completed) ✓
Files Created:
- scripts/evaluate_model.py: Evaluation script (✓)
- smartsynch/utils/evaluation.py: Evaluation metrics (✓)
- tests/test_evaluation.py: Metric unit tests (✓)

### Current Status:
- Model architecture implemented and tested
- Training pipeline completed with configuration
- Evaluation pipeline implemented with metrics
- Ready to proceed with web integration

### 7. Web Integration (Future)
Files Needed:
- smartsynch/api/: FastAPI application
- smartsynch/api/routes/: API endpoints
- docker/: Containerization files

### 8. Continuous Learning (Future)
Files Needed:
- smartsynch/feedback/: Feedback collection
- scripts/retrain.py: Model updating
- tests/test_feedback.py: Feedback tests

graph TB
    subgraph 1_Data_Pipeline[1. Data Pipeline]
        A[Raw Training Data] -->|training_data.json| B[DataProcessor]
        B -->|cleaning.py| C[Text Cleaning]
        B -->|embeddings.py| D[BERT Embeddings]
        B -->|validation.py| E[Data Validation]
        B -->|augmentation.py| F[Data Augmentation]
        C & D & E & F -->|processor.py| G[Processed Dataset]
    end

    subgraph 2_Model_Pipeline[2. Model Training]
        G -->|train_model.py| H[Model Training]
        H -->|classifier.py| I[Base Model]
        I -->|predictor.py| J[Fine-tuning]
        J -->|evaluate_model.py| K[Model Evaluation]
        K -->|evaluation.py| L[Metrics & Analysis]
    end

    subgraph 3_API_Pipeline[3. API Integration]
        L -->|FastAPI| M[Model Serving]
        M -->|routes/| N[API Endpoints]
        N -->|Redis| O[Cache Layer]
        N -->|predictor.py| P[Prediction Service]
    end

    subgraph 4_Frontend[4. Frontend Integration]
        P -->|API Client| Q[Real-time Predictions]
        Q --> R[Category Suggestions]
        R --> S[User Interface]
    end

    subgraph 5_Continuous_Learning[5. Continuous Learning]
        S -->|feedback/| T[User Feedback]
        T -->|user_data.json| U[Feedback Collection]
        U -->|retrain.py| V[Model Retraining]
        V --> J
    end

## Detailed Workflow Explanation

### 1. Data Pipeline
Reference implementation:
```

#### Raw Data Input
- Source: training_data.json containing 100 labeled examples
- Distribution: 20 examples per category (Development, Design, Research)
- Format: Structured JSON with title, description, category fields

#### Data Processing Components
1. Text Cleaning (cleaning.py)
   - Special character removal
   - Whitespace normalization
   - HTML/markdown handling
   - Language detection and validation

2. Embedding Generation (embeddings.py)
   - BERT-based embeddings using Sentence-Transformers
   - Efficient batch processing
   - Embedding caching for performance
   - Dimensionality management

3. Data Validation (validation.py)
   - JSON schema validation
   - Required field verification
   - Category label validation
   - Data quality checks

4. Data Augmentation (augmentation.py)
   - Synonym replacement techniques
   - Back translation methods
   - Random insertion/deletion
   - Dataset balancing

### 2. Model Training Pipeline
Reference implementation:
```

#### Model Architecture
1. Base Model
   - Sentence-Transformer foundation
   - Pre-trained BERT weights
   - Contextual understanding

2. Classification Head
   - Dense layer (128 units)
   - Dropout rate: 0.2
   - Softmax activation
   - Category output

#### Training Process
1. Configuration
   - Hyperparameter loading
   - Data pipeline setup
   - Model initialization

2. Training Loop
   - Batch processing
   - Loss calculation
   - Optimization steps
   - Early stopping

3. Evaluation
   - Accuracy metrics
   - Confusion matrix
   - Cross-validation
   - Performance analysis

### 3. API Integration
Reference implementation:
```

#### FastAPI Application
1. Endpoints
   - Prediction API
   - Batch processing
   - Health checks
   - Feedback collection

2. Performance
   - Redis caching
   - Request validation
   - Error handling
   - Monitoring

### 4. Frontend Integration
Reference implementation:
```

#### Client Components
1. API Client
   - Real-time predictions
   - Error handling
   - Request debouncing

2. User Interface
   - Category suggestions
   - Confidence display
   - Feedback collection

### 5. Continuous Learning
Reference implementation:
```

#### Feedback System
1. Collection
   - Prediction storage
   - User corrections
   - Confidence tracking

2. Model Updates
   - Periodic retraining
   - A/B testing
   - Version control

### Example Data Flow
1. Input: User enters "Add login feature"
2. Processing: 
   - Text cleaning and normalization
   - BERT embedding generation
3. Prediction:
   - Model inference
   - Category: "Development"
   - Confidence scoring
4. Response:
   - API returns prediction
   - UI updates category
5. Feedback:
   - User accepts/rejects
   - Feedback stored
   - Added to retraining data

### Training Guide - Training the Model

#### Prerequisites
1. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Step 1: Data Preparation
1. Ensure your training data is in the correct format:
```json:SmartSynch/data/training_data.json
{
  "samples": [
    {
      "title": "string",
      "description": "string",
      "category": "string"
    }
  ]
}
```

2. Run the data preparation script:
change directory to (tf-env) jmontfort@fedora:~/MyProjects/projectin-ai/ml-training/SmartSynch$ and run

```bash
python -m scripts.prepare_data --input data/training_data.json --output data/processed --test-size 0.2

```

This will:
- Process the training data
- Generate embeddings
- Split into train/val/test splits
- Save processed files in data/processed/
  - X_train.npy: Training embeddings
  - X_val.npy: Validation embeddings
  - y_train.npy: Training labels
  - y_val.npy: Validation labels
  - category_map.npy: Category mapping

#### Step 2: Model Training
1. Configure training parameters in `configs/training_config.yaml`:
```yaml
model:
  dropout_rate: 0.2
  embedding_model: "all-MiniLM-L6-v2"

# Training Parameters
training:
  batch_size: 32
  learning_rate: 0.001
  epochs: 100
  patience: 5  # Early stopping patience
  validation_split: 0.2

# Logging and Checkpoints
logging:
  log_interval: 10  # Log every N batches
  save_best_only: true
  metrics:
    - accuracy
    - precision
    - recall
    - f1

# Early Stopping
early_stopping:
  monitor: "val_loss"
  min_delta: 0.001
  patience: 5
  mode: "min" 
  ```

2. Start the training process:
```bash
python -m scripts.train_model --config configs/training_config.yaml --data-dir data/processed
```

The training script will:
- Load preprocessed data
- Initialize the TaskClassifier model
- Train using the specified configuration
- Save checkpoints to `models/fine_tuned/`

#### Step 3: Model Evaluation
1. Evaluate the trained model:
```bash
# Using separate feature and label files

python -m scripts.evaluate_model \
    --model-path models/fine_tuned/20241128_144942/model.pt \
    --test-data data/processed/X_val.npy \
    --labels data/processed/y_val.npy \
    --output-dir evaluation_results
    
```

This will:
- Load the trained model
- Make predictions on test data
- Generate evaluation metrics:
  - Accuracy, Precision, Recall, F1
  - Confusion matrix plot (saved as confusion_matrix.png)
  - Confidence analysis
- Save detailed results to evaluation_results.json
- Display summary metrics in console output

The evaluation script supports both .npy and .json test data formats and will automatically handle the appropriate data loading and processing.

#### Monitoring Training Progress
- Training metrics are logged to `logs/training.log`
- Monitor metrics using TensorBoard:
```bash
tensorboard --logdir runs/
```

#### Troubleshooting
- If you encounter CUDA out-of-memory errors, reduce batch_size in training_config.yaml
- For poor performance, try adjusting learning_rate or increasing epochs
- Check logs/training.log for detailed error messages

