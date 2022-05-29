from flask import Flask, jsonify

app = Flask(__name__)

port = 8000
scores = {"pete": 4, "john": 1, "timmy": 3, "man": 30, "boy": 12}


@app.route('/scores', methods=['POST'])
def post_scores():
    print("")


@app.route('/scores/<rank>')
def get_scores(rank):
    # Handle errors before sorting scores
    if (not rank.isdigit()) or (int(rank) == 0):
        # Return an error if requested rank is invalid
        return jsonify(error="Requested rank [{}] is invalid, please request a positive integer".format(rank)), 400
    if int(rank) > len(scores):
        # Return an error if requested rank to high
        return jsonify(error="There is no player ranked [{}], please request a lower rank".format(rank)), 400

    # Order scores dict descending
    ordered_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Return name and score of rank index in JSON format
    return jsonify(name=ordered_scores[int(rank) - 1][0],
                   score=ordered_scores[int(rank) - 1][1]), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
