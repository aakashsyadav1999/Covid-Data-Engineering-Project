from src.pipeline.inference_pipeline import InitiateInference

if __name__ == "__main__":
    inti_pipeline = InitiateInference()
    inti_pipeline.fetching_data()
    transformed_data = inti_pipeline.transform_data()
    print(f"This is the transformed data {len(transformed_data)}")
    inti_pipeline.load_data_to_snowflake(transformed_data)