from src.pipeline.inference_pipeline import InitiateInference

if __name__ == "__main__":
    inti_pipeline = InitiateInference()
    raw_data = inti_pipeline.fetching_data()
    print(f"This is the raw data {raw_data}")
