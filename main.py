from services.pipeline import Pipeline

if __name__ == "__main__":
    user_scenery = input("Describe the scenery :")
    pipeline = Pipeline(user_scenery=user_scenery)
    pipeline.run()