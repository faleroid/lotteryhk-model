from flask import Flask, render_template, request
from config import Config
from utils import BallUtils
from services import LotteryPredictor

app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER, static_folder='../static')
predictor = LotteryPredictor()

@app.route('/', methods=['GET', 'POST'])
def index():
    years, valid_dates = predictor.get_available_dates()
    
    result = None
    error = None

    if request.method == 'POST':
        try:
            date_str = f"{request.form.get('year')}-{int(request.form.get('month')):02d}-{int(request.form.get('day')):02d}"

            pred, true_vals, data_source = predictor.predict(date_str)
            
            acc = len(set(pred) & set(true_vals))
            
            main_true = true_vals[:6]
            spec_true = true_vals[6] if len(true_vals) > 6 else None

            pred_set = set(pred)
            true_set = set(true_vals)
            
            pred_balls_formatted = BallUtils.format_balls_data(pred)
            for ball in pred_balls_formatted:
                if ball['num'] not in true_set:
                    ball['color'] = 'ball-gray'
            
            true_balls_formatted = BallUtils.format_balls_data(main_true)
            for ball in true_balls_formatted:
                if ball['num'] not in pred_set:
                    ball['color'] = 'ball-gray'
            
            special_ball_data = None
            if spec_true:
                sp_color = 'ball-purple'
                if spec_true not in pred_set:
                    sp_color = 'ball-gray'
                special_ball_data = {'num': spec_true, 'color': sp_color}

            result = {
                'date': date_str,
                'data_source': data_source,
                'pred_balls': pred_balls_formatted,
                'true_balls': true_balls_formatted,
                'special_ball': special_ball_data,
                'accuracy': acc
            }
        except Exception as e:
            error = str(e)

    return render_template('index.html', years=years, valid_dates=valid_dates, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)