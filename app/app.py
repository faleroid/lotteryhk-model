from flask import Flask, render_template, request
from config import Config
from utils import BallUtils
from services import LotteryPredictor

app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER)
predictor = LotteryPredictor()

@app.route('/', methods=['GET', 'POST'])
def index():
    years, valid_dates = predictor.get_available_dates()
    
    result = None
    error = None

    if request.method == 'POST':
        try:
            date_str = f"{request.form.get('year')}-{int(request.form.get('month')):02d}-{int(request.form.get('day')):02d}"

            pred, true_vals = predictor.predict(date_str)
            
            acc = len(set(pred) & set(true_vals))
            
            main_true = true_vals[:6]
            spec_true = true_vals[6] if len(true_vals) > 6 else None

            result = {
                'date': date_str,
                'pred_balls': BallUtils.format_balls_data(pred),
                'true_balls': BallUtils.format_balls_data(main_true),
                'special_ball': {'num': spec_true, 'color': 'ball-purple'} if spec_true else None,
                'accuracy': acc
            }
        except Exception as e:
            error = str(e)

    return render_template('index.html', years=years, valid_dates=valid_dates, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)