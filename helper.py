import pandas as pd
import numpy as np
import joblib

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
    def impute_data_(X):
        mice_kernel = ImputationKernel(data=X, num_datasets=3, save_all_iterations_data=True, random_state=57)
        mice_kernel.mice(iterations=15, n_estimators=30)
        X = mice_kernel.complete_data()
        return X

    print('welcome to our service. Please fill your car info correctly.')
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

