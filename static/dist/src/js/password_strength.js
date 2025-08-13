const password_input = document.getElementById("pswrd_str_password")
const entropy_output = document.getElementById("render_entropy")
const points_output = document.getElementById("render_points")
const dict_output = document.getElementById("render_dict_check")
const final_score_output = document.getElementById("render_final_score")

/**
 * Calculates a points score for a passowrd.
 * @param {String} password - the password
 * @returns number of points password scored
 */
function get_points(password) {
    let points = 0;
    const L = password.length;

    if (L >= 8) points++
    if (L >= 12) points++
    if (/[A-Z]/.test(password)) points++
    if (/[a-z]/.test(password)) points++
    if (/[0-9]/.test(password)) points++
    if (/[{}\[\]()#:;^,.?!|&_`~@$%\/\\=+\*'"<>-]/.test(password)) points += 2

    return points;
}

function points_rating(points) {
    switch (true) {
        case 6 <= points:
            return {"rank": "Strong", "score": 2};
        case 3 <= points && points <= 5:
            return {"rank": "Moderate", "score": 1};
        default:
            return {"rank": "Weak", "score": 0};
    }
}

/**
 * Calculates the entropy of a password using the formula
 * E = L * log2(C) where E = Entropy, L = Length of String, and C = Char Set Size
 * @param {String} password - the password to get entropy of
 * @returns The entropy in bits
 */
function get_entropy(password) {
    const L = password.length
    const C = 52 + 10 + 33 // num upper and lower chars, num digits, and num special chars
    return L * Math.log2(C)
}

function entropy_rating(entropy) {
    switch (true) {
        case 80 <= entropy:
            return {"rank": "Strong", "score": 4};
        case 65 <= entropy:
            return {"rank": "Moderate", "score": 3};
        case 36 <= entropy && entropy <= 59:
            return {"rank": "Alright", "score": 2};
        case 28 <= entropy && entropy <= 35:
            return {"rank": "Weak", "score": 1};
        default:
            return {"rank": "Very Weak", "score": 0};
    }
}

/**
 * Calculates a result incrementing every time either number crosses an even boundary
 * @param {Number} A - The first number to compare
 * @param {Number} B - The second number to compare
 * @returns score
 */
function calc_score(A, B) {
    return Math.floor(A / 2) + Math.floor(B / 2)
}

function rating_scale_five(num) {
    ranks = ["Very Weak", "Weak", "Alright", "Moderate", "Strong"]
    return {"rank": ranks[num], "score": num}
}

/**
 * Calculates a score based on three criterea
 * @param {Number} entropy_rating - the password's entropy rating, on a scale of 0-5
 * @param {Number} points - the password's points rating, on a scale of 0-7
 * @param {Number} pattern_score - the password's pattern rating, on a scale of 0-4
 * @returns score dict composed of a String rank and Number score
 */
function combined_score(entropy, points, pattern) {

    // How important each component is to final score
    const weight_entropy = 0.75;
    const weight_points = 1;
    const weight_pattern = 2;

    // reduce ranges for simpler calculations
    if (4 <= entropy) entropy_score = 3;
    else if (2 <= entropy) entropy_score = 2;
    else entropy_score = 1;

    if (6 <= points) points_score = 3;
    else if (3 <= points) points_score = 2;
    else points_score = 1;

    if (pattern == 4) pattern_score = 3;
    else if (2 <= pattern) pattern_score = 2;
    else pattern_score = 1;

    const maxScore = weight_entropy * 3 + weight_points * 3 + weight_pattern * 3;
    const raw = entropy_score * weight_entropy
        + points_score * weight_points
        + pattern_score * weight_pattern;
    const normalized = raw/maxScore;
    const in_range = Math.floor(normalized * 5) - 1;
    console.log(`entropy: ${entropy_score}, points: ${points_score}, pattern: ${pattern_score}\nmax: ${maxScore}\nraw: ${raw}, normalized: ${normalized}, range: ${in_range}`)
    return rating_scale_five(in_range);
}

/**
 * Rounds a number to a specified amount of decimal spaces
 * @param {Number} num - the number
 * @param {Number} place - how many decimal places to round to
 * @returns 
 */
function round_decimal(num, place) {
    return Math.ceil(num * place) / place
}

password_input.addEventListener('keyup', function(k) {
    const password = password_input.value;
    const entropy_whole = Math.floor(get_entropy(password))
    
    const entropy = round_decimal(get_entropy(password) % 1, 8) + entropy_whole
    entropy_output.innerHTML = `${entropy} (${entropy_rating(entropy)["rank"]})`;

    const points = get_points(password);
    points_output.innerHTML = `${points} (${points_rating(points)["rank"]})`

    const pattern_check = zxcvbn(password);
    dict_output.innerHTML = `${pattern_check.score} (${rating_scale_five(pattern_check.score)["rank"]})`;

    const final_score = combined_score(entropy_rating(entropy)["score"], points, pattern_check.score)
    final_score_output.innerHTML = `${final_score["score"]} (${final_score["rank"]})`;
})