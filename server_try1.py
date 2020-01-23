from flask import Flask, request, render_template, Markup
import pandas as pd
import csv
app = Flask(__name__)
file_path ="./sensor_data.csv"
my_port = 19886
#df=pd.read_csv('sensor_data.csv')
#labels = df['time']
#Values=df['lux']

#return HTML 
@app.route('/', methods=['GET'])
def get_html():
    df = pd.read_csv("sensor_data.csv", names = ['time', 'lux'])
    labels = df.ix[:, 'time']
    sensorvalues = df.ix[:, 'lux']
    #labels=labels
    #sensorvalues=sensorvalues
    #print(df)
    try:
        f = open('sensor_data.csv', 'r')
        for row in f:
            lux = row
    except Exception as e:
        print(e)
        return e
    finally:
        f.close()
    values = lux.split(',')
    return render_template('./try1.html', title='Illuminance Sensor Data',values=values, labels=labels, sensorvalues = sensorvalues)


#receive sensor data 
@app.route('/lux', methods=['POST'])
def update_lux():
    try:
        time = request.form["time"]
        lux = request.form["lux"]
    except Exception as e:
        
        return "parameter is incorrect"
    try:
        f = open(file_path, 'a')
        f.write(time + "," + lux +"\n")
        return "Success to write!"
    except Exception as e:
        print(e)
        return "failed to write"
    finally:
        f.close()
    return get_html()


#reading and retrieve sensor data
@app.route('/lux', methods=['GET'])
def get_lux():
    try:
        f = open(file_path, 'r')
        for row in f:
            lux = row
        return lux
    except Exception as e:
        print(e)
        return e
    finally:
        f.close()

def create_csv():
    with open('sensor_data.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow([get_lux()])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=my_port)