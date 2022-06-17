from flask import Flask, jsonify, request
from flask_caching import Cache
from marshmallow import Schema, fields, ValidationError
from marshmallow.validate import Range

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'  # Use simple caching that uses a hashmap
cache = Cache()
cache.init_app(app)

port = 8888
host = "0.0.0.0"
scores = {"pete": 4, "john": 1, "timmy": 3}  # Some initial data for testing


# Schema used to validate scores POST payload so only specified fields are accepted
class ScoreSchema(Schema):
    name = fields.String(required=True, allow_none=False)
    score = fields.Integer(required=True, allow_none=False,
                           validate=[Range(min=1, error="Value must be greater than 0")])


@app.route('/scores/', methods=['POST'])
def post_scores():
    schema = ScoreSchema()

    try:
        # Validate request body against score schema data types
        result = schema.load(request.json)
    except ValidationError as e:
        # Return an error with reasoning if validation fails
        return jsonify(error="Scores POST request invalid", reason=e.messages), 400

    try:
        if int(result.get("score")) <= scores[result.get("name")]:
            # Return an info message if incoming score is lower than what is currently recorded for the name
            return jsonify(info="A higher score for this player has been recorded, system will not update"), 200
    except KeyError:
        pass  # Catch KeyError that will be thrown if name is not already stored, do nothing...

    # If validation passes, add the score to the dictionary
    scores[result.get("name")] = int(result.get("score"))

    return jsonify(success="System has been updated. Score: [{}]".format(result)), 200


@app.route('/scores/<rank>/', methods=['GET'])
@cache.memoize(timeout=60)  # Use memoize to use argument as cache key as well
def get_scores(rank):
    print("Cache not used")
    # Handle errors before sorting scores
    if (not rank.isdigit()) or (int(rank) == 0):
        # Return an error if requested rank is invalid
        return jsonify(
            error="Requested rank [{}] is invalid, please request a positive non zero integer".format(rank)), 400
    if int(rank) > len(scores):
        # Return an error if requested rank to high
        return jsonify(error="There is no player ranked [{}]".format(rank)), 400

    # Order scores dict descending
    ordered_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Return name and score of rank index in JSON format
    return jsonify(name=ordered_scores[int(rank) - 1][0],
                   score=ordered_scores[int(rank) - 1][1]), 200


if __name__ == '__main__':
    app.run(host=host, port=port)
