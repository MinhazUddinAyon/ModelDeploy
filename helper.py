import pandas as pd
import numpy as np
import joblib
import time
from sklearn.pipeline import Pipeline


def object_cat(df):
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].astype('category')

# Load the pipeline from the file
pipe = joblib.load('optimized_pipeline.joblib')
X = joblib.load('optimized_X.joblib')

def maker_name(name):
    return list(X[name].unique())


def HTML():
    return X.to_html(classes='table table-striped', index=False)


def process_data(one_df):
    from miceforest import ImputationKernel
    def impute_data_(X):
        mice_kernel = ImputationKernel(data=X, num_datasets=3, save_all_iterations_data=True, random_state=57)
        mice_kernel.mice(iterations=15, n_estimators=30)
        X = mice_kernel.complete_data()
        return X

    print('welcome to our service. Please fill your car info correctly.')
    if pd.Series(one_df.values[0]).count() < 17:
        if len(X.groupby('Maker').get_group(one_df['Maker'].iloc[0])) > 1:

            # Get the nan column names
            missing = []
            for i in one_df.columns:
                if one_df[i].fillna(0)[0] == 0.0:
                    missing.append(i)

            print('You have missing values. Please wait to impute...')
            start_time = time.time()
            if one_df['Bodytype'].fillna(0)[0] == 0.0:
                one_df = pd.concat([X.groupby('Genmodel').get_group(one_df['Genmodel'].iloc[0]), one_df],
                                   ignore_index=True)
                object_cat(one_df)
                one_df = impute_data_(one_df)
                one_df = one_df.iloc[-1].to_frame().transpose()
            else:
                one_df = pd.concat([X.groupby(['Genmodel', 'Bodytype']).get_group(
                    tuple(one_df[['Genmodel', 'Bodytype']].iloc[0].values)), one_df], ignore_index=True)
                object_cat(one_df)
                one_df = impute_data_(one_df)
                one_df = one_df.iloc[-1].to_frame().transpose().reset_index().drop(columns=['index'])

            end_time = time.time()
            execution_time = end_time - start_time

            print(f"Time get for filling missing information: {execution_time:.4f} seconds")
            for j in missing:
                print(f"You missed to provide information: {j}, which is filling by: {one_df[j].values[0]}")
            print(f"Information filling from {len(X.groupby('Maker').get_group(one_df['Maker'].iloc[0]))} stored data")
        else:
            print('Please provides your all information.')

    one_df['Runned_Miles'] = np.sqrt(one_df['Runned_Miles'].values[0])
    one_df['Engine_size'] = np.log1p(one_df['Engine_size'].values[0])
    one_df['Engine_power'] = np.log1p(one_df['Engine_power'].values[0])

    return one_df


def make_prediction(maker, genmodel, bodytype, gearbox, fuel_type, runned_miles, engine_size, engine_power, average_mpg,
                    top_speed, wheelbase,
                    height, width, length, seat_num, door_num, cars_old):
    data = {
        'Maker': maker,
        'Genmodel': genmodel,
        'Bodytype': bodytype,
        'Gearbox': gearbox,
        'Fuel_type': fuel_type,
        'Runned_Miles': runned_miles,
        'Engine_size': engine_size,
        'Engine_power': engine_power,
        'Average_mpg': average_mpg,
        'Top_speed': top_speed,
        'Wheelbase': wheelbase,
        'Height': height,
        'Width': width,
        'Length': length,
        'Seat_num': seat_num,
        'Door_num': door_num,
        'Cars_old': cars_old
    }
    df = pd.DataFrame(data, index=[0])
    df = process_data(df)
    return round(np.expm1(pipe.predict(df)[0]), 2)


'''    Genmodel = request.args.get('genmodel')
    Bodytype = request.args.get('bodytype')
    Gearbox = request.args.get('gearbox')
    Fuel_type = request.args.get('fuel_type')
    Runned_Miles = float(request.args.get('runned_miles'))
    Engine_size = float(request.args.get('engine_size'))
    Engine_power = float(request.args.get('engine_power'))
    Average_mpg = request.args.get('average_mpg')
    Top_speed = float(request.args.get('top_speed'))
    Wheelbase = float(request.args.get('wheelbase'))
    Height = float(request.args.get('height'))
    Width = float(request.args.get('width'))
    Length = float(request.args.get('length'))
    Seat_num = float(request.args.get('seat_num'))
    Door_num = float(request.args.get('door_num'))
    Cars_old = request.args.get('cars_old')

        try:
        return print(f'Your car price approximately: {round(np.expm1(pipe.predict(df)[0]),2)}$(dollar)')
    except:
        return print('Sorry! No car available in this name.')

    '''