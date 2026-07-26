import re

SUBJECT_KEYWORDS = {
    "Mathematics": [
        "math", "mathematics", "maths", "algebra", "equation", "fraction",
        "fractions", "geometry", "calculus", "statistics", "solve for",
        "variable", "numerator", "denominator", "addition", "subtraction",
        "multiplication", "division", "mean", "median", "mode", "average",
        "percentage", "percent", "decimal", "ratio", "proportion",
        "perimeter", "area", "volume", "angle", "triangle", "square",
        "circle", "graph", "chart", "data", "probability", "number",
        "counting", "place value", "rounding", "estimate", "measurement",
        "length", "mass", "weight", "capacity", "time", "money", "shape",
        "symmetry", "pattern", "sequence", "set", "whole number", "integer",
        "prime", "multiple", "factor", "power", "index", "square root",
        "pythagoras", "pythagorean", "hypotenuse",
        "negative", "bracket", "formula", "inequality", "function",
        "coordinate", "bearing", "scale", "speed", "distance", "simple interest",
    ],
    "Science": [
        "science", "biology", "chemistry", "physics", "scientific", "experiment",
        "photosynthesis", "cell", "cells", "mitosis", "meiosis", "gravity",
        "water cycle", "evaporation", "condensation", "precipitation",
        "solar system", "planet", "orbit", "digestion", "digestive",
        "respiratory", "respiration", "atoms", "molecules", "elements",
        "force", "energy", "motion", "magnet", "electricity", "circuit",
        "habitat", "ecosystem", "food chain", "living things", "organisms",
        "skeleton", "muscle", "nervous system", "blood", "heart", "lungs",
        "mineral", "rock", "volcano", "earthquake", "classification",
        "mammal", "reptile", "amphibian", "bird", "fish", "plant",
        "flower", "seed", "germination", "pollination", "dispersal",
        "material", "solid", "liquid", "gas", "states of matter",
        "sound", "light", "reflection", "refraction", "circuit",
        "conductor", "insulator", "friction", "machine", "lever",
        "pulley", "skeleton", "joint", "nutrition", "food", "diet",
    ],
    "English": [
        "english", "grammar", "vocabulary", "spelling", "reading", "writing",
        "noun", "verb", "adjective", "sentence", "paragraph", "essay",
        "comprehension", "literature", "adverb", "pronoun", "preposition",
        "conjunction", "tense", "tenses", "punctuation", "comma", "full stop",
        "question mark", "apostrophe", "speech", "poem", "story", "letter",
        "summary", "figure of speech", "simile", "metaphor", "idiom",
        "synonym", "antonym", "prefix", "suffix", "homophone", "rhyme",
        "drama", "prose", "dialogue", "interview", "report", "instruction",
        "persuasive", "narrative", "descriptive", "topic sentence",
        "main idea", "detail", "conclusion", "introduction",
    ],
    "Social Studies": [
        "social studies", "history", "geography", "government", "civics",
        "milton margai", "sierra leone", "independence", "democracy",
        "culture", "tradition", "map", "maps", "climate", "weather",
        "population", "settlement", "transport", "communication",
        "natural resource", "mining", "agriculture", "trade", "import", "export",
        "freetown", "district", "province", "chiefdom", "constitution",
        "president", "parliament", "election", "vote", "citizen",
        "right", "responsibility", "colonial", "slave", "abolition",
        "peace", "conflict", "refugee", "development", "economy",
        "tax", "budget", "bank", "savings", "family", "community",
        "religion", "ethnic", "migration", "urban", "rural", "industry",
        "tourism", "conservation", "environment", "pollution", "recycling",
    ],
    "Vocational": [
        "vocational", "trade", "craft", "carpentry", "tailoring", "farming",
        "agriculture", "business", "entrepreneur", "sewing", "building",
        "construction", "plumbing", "welding", "cooking", "baking",
        "soap making", "tie dye", "batik", "leather", "pottery",
        "carpenter", "tailor", "farmer", "bricklayer", "mason",
        "electrician", "mechanic", "painting", "decorating", "fishing",
        "food preservation", "marketing", "bookkeeping", "customer",
        "poultry", "livestock", "vegetable", "crop", "harvest",
        "tool", "maintenance", "workshop", "apprentice", "skill",
        "handicraft", "basket weaving", "mat making", "beadwork",
        "catering", "hotel", "tourism", "beauty", "hair dressing",
    ],
}


def _classify_subject(message: str) -> str | None:
    for subject, keywords in SUBJECT_KEYWORDS.items():
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", message, re.IGNORECASE):
                return subject
    return None


RESPONSES = [

# ╔══════════════════════════════════════════════════════════════╗
# ║                     SUBJECT: GENERAL                       ║
# ╚══════════════════════════════════════════════════════════════╝

    {
        "subject": "General",
        "keywords": ["hello", "hi", "hey", "greeting", "good morning", "good afternoon", "good evening", "how are you"],
        "response": (
            "Hello and welcome to VisionLearn. I am your AI learning assistant. "
            "I am here to help you with your school subjects including Mathematics, Science, English, Social Studies, and Vocational Studies. "
            "Please feel free to ask me any question about your studies."
        ),
    },
    {
        "subject": "General",
        "keywords": ["who are you", "what are you", "what can you do", "tell me about yourself"],
        "response": (
            "I am VisionLearn, an AI educational assistant designed to help students at the Milton Margai School for the Blind in Sierra Leone. "
            "I can help you with all your school subjects: Mathematics, Science, English, Social Studies, and Vocational Studies. "
            "Just tell me what subject you are studying and what you would like to learn about, and I will explain it clearly and simply."
        ),
    },
    {
        "subject": "General",
        "keywords": ["thank", "thanks", "thank you"],
        "response": (
            "You are very welcome. I am always here to help you with your learning. "
            "Keep up the great work and never stop asking questions. That is how we learn and grow."
        ),
    },
    {
        "subject": "General",
        "keywords": ["bye", "goodbye", "see you", "good night", "see you later"],
        "response": (
            "Goodbye and keep learning. Remember that every day is a chance to learn something new. "
            "Come back anytime you need help with your studies."
        ),
    },
    {
        "subject": "General",
        "keywords": ["pythagorean theorem", "pythagoras"],
        "response": (
            "The Pythagorean theorem is a rule about right-angled triangles. "
            "It states that the square of the hypotenuse (longest side) equals the sum of the squares of the other two sides. "
            "The formula is a squared plus b squared equals c squared, where c is the hypotenuse. "
            "For example, if a is 3 and b is 4, then c squared is 9 plus 16 equals 25, so c is the square root of 25, which is 5. "
            "This theorem is used to find the length of a side in a right triangle when you know the other two sides."
        ),
    },

# ╔══════════════════════════════════════════════════════════════╗
# ║                   SUBJECT: MATHEMATICS                      ║
# ╚══════════════════════════════════════════════════════════════╝

    # ─── Numbers and Place Value ───

    {
        "subject": "Mathematics",
        "keywords": ["place value", "value of a digit", "expanded form"],
        "response": (
            "Place value is the value of a digit based on its position in a number. "
            "In the number 3,456, the digit 3 is in the thousands place and means 3,000. "
            "The digit 4 is in the hundreds place and means 400. The digit 5 is in the tens place and means 50. "
            "The digit 6 is in the ones place and means 6. "
            "We can write 3,456 in expanded form as 3,000 plus 400 plus 50 plus 6. "
            "Understanding place value helps you read, write, and compare large numbers."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["rounding", "round", "estimate", "estimation"],
        "response": (
            "Rounding is a way to make a number simpler but still close to its original value. "
            "To round a number to the nearest ten, look at the ones digit. If it is 5 or more, round up, otherwise round down. "
            "For example, 37 rounded to the nearest ten is 40 because the ones digit is 7, which is 5 or more. "
            "34 rounded to the nearest ten is 30 because the ones digit is 4. "
            "Estimation means using rounded numbers to get an approximate answer without calculating exactly."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["prime number", "prime", "composite number", "composite"],
        "response": (
            "A prime number is a number that has exactly two factors: 1 and itself. "
            "For example, 2, 3, 5, 7, 11, 13, 17, and 19 are prime numbers. "
            "The number 2 is the only even prime number. "
            "A composite number has more than two factors. For example, 4 has factors 1, 2, and 4. "
            "The number 1 is neither prime nor composite."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["multiple", "multiples", "factor", "factors", "common factor", "common multiple", "LCM", "HCF", "lowest common", "highest common"],
        "response": (
            "A factor is a number that divides exactly into another number. For example, the factors of 12 are 1, 2, 3, 4, 6, and 12. "
            "A multiple is a number you get when you multiply a number by another. For example, the multiples of 3 are 3, 6, 9, 12, and so on. "
            "The highest common factor, or HCF, is the largest number that divides two numbers exactly. For 12 and 18, the HCF is 6. "
            "The lowest common multiple, or LCM, is the smallest number that is a multiple of two numbers. For 4 and 6, the LCM is 12."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["negative number", "negative", "positive", "integer", "integers", "number line"],
        "response": (
            "Integers are whole numbers that can be positive, negative, or zero. "
            "Positive numbers are greater than zero, like 1, 2, 3. Negative numbers are less than zero, like negative 1, negative 2, negative 3. "
            "A number line shows numbers in order. Zero is in the middle. Numbers to the right are positive, and numbers to the left are negative. "
            "When you add a negative number, you move left on the number line. When you subtract a negative number, you move right. "
            "For example, 5 plus negative 3 equals 2, and 5 minus negative 3 equals 8."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["power", "index", "indices", "exponent", "square", "square root", "cubed", "cube root"],
        "response": (
            "A power or index tells you how many times to multiply a number by itself. "
            "For example, 3 to the power of 2 means 3 times 3, which equals 9. We say 3 squared equals 9. "
            "3 to the power of 3 means 3 times 3 times 3, which equals 27. We say 3 cubed equals 27. "
            "A square root is the opposite of squaring. The square root of 9 is 3 because 3 times 3 equals 9. "
            "A cube root is the opposite of cubing. The cube root of 27 is 3 because 3 times 3 times 3 equals 27."
        ),
    },

    # ─── Operations ───

    {
        "subject": "Mathematics",
        "keywords": ["pythagorean theorem", "pythagoras"],
        "response": (
            "The Pythagorean theorem is a rule about right-angled triangles. "
            "It states that the square of the hypotenuse (longest side) equals the sum of the squares of the other two sides. "
            "The formula is a squared plus b squared equals c squared, where c is the hypotenuse. "
            "For example, if a is 3 and b is 4, then c squared is 9 plus 16 equals 25, so c is the square root of 25, which is 5. "
            "This theorem is used to find the length of a side in a right triangle when you know the other two sides."
        ),
    },

    {
        "subject": "Mathematics",
        "keywords": ["addition", "add", "plus", "sum", "adding"],
        "response": (
            "Addition is combining two or more numbers to find the total or sum. "
            "The symbol for addition is the plus sign. For example, 3 plus 5 equals 8. "
            "When adding larger numbers, line them up by place value. Add each column starting from the right. "
            "If a column adds up to 10 or more, carry the extra digit to the next column on the left. "
            "Addition is the opposite of subtraction. You can check your answer by subtracting one of the numbers from the sum."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["subtraction", "subtract", "minus", "difference", "take away"],
        "response": (
            "Subtraction is taking one number away from another to find the difference. "
            "The symbol for subtraction is the minus sign. For example, 8 minus 3 equals 5. "
            "When subtracting larger numbers, line them up by place value. Subtract each column starting from the right. "
            "If the top digit is smaller than the bottom digit, borrow 1 from the next column. "
            "Subtraction is the opposite of addition. You can check your answer by adding the difference back to the number you subtracted."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["multiplication", "multiply", "times", "product", "multiplying"],
        "response": (
            "Multiplication is adding the same number many times. For example, 3 times 4 means 3 plus 3 plus 3 plus 3, which equals 12. "
            "The symbol for multiplication is the times sign. The numbers you multiply are called factors, and the answer is called the product. "
            "Learning your times tables from 1 to 12 is very important. Here are some tips: "
            "Any number times 0 equals 0. Any number times 1 equals itself. "
            "To multiply by 10, add a zero at the end. For example, 7 times 10 equals 70. "
            "Multiplication is the opposite of division."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["division", "divide", "quotient", "dividing", "remainder", "long division"],
        "response": (
            "Division is splitting a number into equal parts. For example, 12 divided by 3 means splitting 12 into 3 equal groups, which gives 4 in each group. "
            "The number being divided is called the dividend. The number you are dividing by is called the divisor. The answer is called the quotient. "
            "If a number does not divide exactly, you get a remainder. For example, 13 divided by 3 is 4 remainder 1. "
            "Long division is a method for dividing larger numbers. You divide, multiply, subtract, and bring down the next digit, repeating until done. "
            "Division is the opposite of multiplication."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["order of operations", "BODMAS", "BIDMAS", "PEMDAS", "brackets"],
        "response": (
            "Order of operations tells us which calculation to do first when solving a problem. "
            "The rule is BODMAS: Brackets first, then Orders which are powers and square roots, then Division and Multiplication from left to right, then Addition and Subtraction from left to right. "
            "For example, in 3 plus 4 times 2, multiplication comes first, so 4 times 2 equals 8, then 3 plus 8 equals 11. "
            "If we had brackets, like 3 plus 4 in brackets times 2, we would do the bracket first: 3 plus 4 equals 7, then 7 times 2 equals 14."
        ),
    },

    # ─── Fractions, Decimals, Percentages ───

    {
        "subject": "Mathematics",
        "keywords": ["fraction", "fractions", "proper fraction", "improper fraction", "mixed number"],
        "response": (
            "A fraction represents a part of a whole. For example, if you cut a cake into 4 equal pieces and eat 1 piece, you have eaten one quarter of the cake. "
            "We write this as the fraction 1 over 4. The top number is called the numerator and it tells you how many parts you have. "
            "The bottom number is called the denominator and it tells you how many equal parts the whole is divided into. "
            "A proper fraction has a numerator smaller than the denominator, like 3 over 4. "
            "An improper fraction has a numerator larger than the denominator, like 7 over 4. "
            "A mixed number has a whole number and a fraction, like 1 and 3 over 4. To convert an improper fraction to a mixed number, divide the numerator by the denominator."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["equivalent fraction"],
        "response": (
            "Equivalent fractions are fractions that represent the same value even though they look different. "
            "For example, 1 over 2, 2 over 4, and 3 over 6 are all equivalent fractions because they all mean half. "
            "To find an equivalent fraction, multiply or divide both the numerator and denominator by the same number. "
            "To simplify a fraction, divide the numerator and denominator by their highest common factor. "
            "For example, 4 over 8 simplifies to 1 over 2 by dividing both numbers by 4."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["add fraction", "subtract fraction", "adding fractions", "subtracting fractions"],
        "response": (
            "To add or subtract fractions, the denominators must be the same. "
            "If the denominators are different, find the lowest common denominator first. "
            "For example, to add 1 over 4 and 1 over 2, the lowest common denominator is 4. Convert 1 over 2 to 2 over 4. Then 1 over 4 plus 2 over 4 equals 3 over 4. "
            "Once the denominators are the same, add or subtract only the numerators. The denominator stays the same. "
            "If the answer is an improper fraction, convert it to a mixed number."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["multiply fraction", "multiplying fractions"],
        "response": (
            "To multiply fractions, multiply the numerators together and multiply the denominators together. "
            "For example, 1 over 2 times 3 over 4 equals 1 times 3 over 2 times 4, which is 3 over 8. "
            "If you are multiplying a whole number by a fraction, write the whole number as a fraction over 1. For example, 3 times 1 over 4 is 3 over 1 times 1 over 4, which is 3 over 4. "
            "Always simplify your answer if possible."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["divide fraction", "dividing fractions"],
        "response": (
            "To divide fractions, flip the second fraction upside down, which means find its reciprocal, and then multiply. "
            "For example, 1 over 2 divided by 3 over 4 becomes 1 over 2 times 4 over 3, which equals 4 over 6, which simplifies to 2 over 3. "
            "The reciprocal of a fraction is created by swapping the numerator and denominator. The reciprocal of 2 over 3 is 3 over 2. "
            "If dividing a whole number by a fraction, write the whole number as a fraction over 1 first."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["decimal", "decimals", "decimal place", "decimal point", "recurring"],
        "response": (
            "A decimal is a way of writing a number that is not a whole number, using a decimal point. "
            "For example, 0.5 means half, 0.25 means one quarter, and 0.75 means three quarters. "
            "The first digit after the decimal point is the tenths place, the second is the hundredths place, and the third is the thousandths place. "
            "To add or subtract decimals, line up the decimal points vertically and then add or subtract as usual. "
            "To multiply decimals, multiply as normal and then count the total number of digits after the decimal points in both numbers. "
            "To divide decimals, move the decimal point in both numbers to make the divisor a whole number."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["percentage", "percent", "percentage increase", "percentage decrease"],
        "response": (
            "A percentage is a way of expressing a number as a part of 100. The word percent means out of 100. "
            "For example, 50 percent means 50 out of 100, which is half. "
            "To find a percentage of a number, multiply the number by the percentage divided by 100. For example, 20 percent of 80 is 80 times 20 over 100, which equals 16. "
            "To convert a fraction to a percentage, divide the numerator by the denominator and multiply by 100. "
            "Percentage increase adds a percentage of the original amount. Percentage decrease subtracts it. "
            "For example, a 10 percent increase of 100 is 110. A 10 percent decrease of 100 is 90."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["ratio", "proportion", "rate"],
        "response": (
            "A ratio compares two quantities. For example, if there are 2 boys and 3 girls in a group, the ratio of boys to girls is 2 to 3. "
            "We write this as 2 colon 3. Ratios can be simplified just like fractions. For example, the ratio 4 to 6 simplifies to 2 to 3. "
            "A proportion is an equation that says two ratios are equal. For example, 2 over 4 equals 1 over 2 is a proportion. "
            "A rate compares two quantities with different units. For example, speed is a rate because it compares distance to time, like 60 kilometres per hour."
        ),
    },

    # ─── Algebra ───

    {
        "subject": "Mathematics",
        "keywords": ["algebra", "algebraic", "algebraic expression"],
        "response": (
            "Algebra is a branch of mathematics where we use letters to represent unknown numbers. These letters are called variables. "
            "For example, in x plus 3 equals 7, the letter x is a variable. "
            "An algebraic expression combines numbers, variables, and operations, like 3x plus 5. "
            "Like terms have the same variable. For example, 3x and 7x are like terms and can be combined: 3x plus 7x equals 10x. "
            "Unlike terms, like 3x and 5y, cannot be combined."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["equation", "solve", "solving", "solution", "unknown"],
        "response": (
            "An equation states that two expressions are equal, with an equals sign in between. "
            "To solve an equation, find the value of the variable that makes the equation true. "
            "Keep the equation balanced by doing the same operation to both sides. "
            "For example, to solve x plus 5 equals 12, subtract 5 from both sides to get x equals 7. "
            "To solve 3x equals 15, divide both sides by 3 to get x equals 5. "
            "For two-step equations like 2x plus 3 equals 11, first subtract 3 from both sides to get 2x equals 8, then divide by 2 to get x equals 4."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["inequality", "inequalities", "greater than", "less than"],
        "response": (
            "An inequality shows that two values are not equal. The symbols are greater than, less than, greater than or equal to, and less than or equal to. "
            "For example, x greater than 5 means x can be any number bigger than 5. "
            "To solve inequalities, use the same rules as equations, with one important difference: if you multiply or divide by a negative number, flip the inequality sign. "
            "For example, negative x greater than 5 becomes x less than negative 5 after dividing by negative 1 and flipping the sign."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["formula", "formulae", "subject of formula"],
        "response": (
            "A formula is a rule that shows the relationship between two or more quantities. "
            "For example, the formula for area of a rectangle is A equals L times W, where A is area, L is length, and W is width. "
            "Changing the subject of a formula means rearranging it so a different variable is on its own. "
            "For example, if A equals L times W and we want W as the subject, we write W equals A divided by L. "
            "You use the same inverse operations as solving equations."
        ),
    },

    # ─── Geometry ───

    {
        "subject": "Mathematics",
        "keywords": ["geometry", "geometric"],
        "response": (
            "Geometry is the branch of mathematics that deals with shapes, sizes, and properties of space. "
            "A point is a location in space. A line is a straight path of points that goes on forever in both directions. "
            "A line segment is part of a line with two endpoints. A ray starts at one point and goes on forever in one direction. "
            "An angle is formed where two lines meet. Angles are measured in degrees. "
            "A right angle is 90 degrees, an acute angle is less than 90 degrees, and an obtuse angle is between 90 and 180 degrees."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["triangle", "triangles", "types of triangle"],
        "response": (
            "A triangle is a three-sided shape. The three angles inside a triangle always add up to 180 degrees. "
            "There are different types of triangles based on sides: an equilateral triangle has all three sides equal, an isosceles triangle has two equal sides, "
            "and a scalene triangle has all sides different. "
            "Based on angles, an acute triangle has all angles less than 90 degrees, a right-angled triangle has one 90 degree angle, "
            "and an obtuse triangle has one angle greater than 90 degrees. "
            "The area of a triangle is half times base times height."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["quadrilateral", "quadrilaterals", "square", "rectangle", "parallelogram", "rhombus", "trapezium", "kite"],
        "response": (
            "A quadrilateral is a four-sided shape. The angles inside a quadrilateral always add up to 360 degrees. "
            "A square has four equal sides and four right angles. A rectangle has opposite sides equal and four right angles. "
            "A parallelogram has opposite sides equal and parallel. A rhombus has all sides equal but angles are not necessarily 90 degrees. "
            "A trapezium has one pair of parallel sides. A kite has two pairs of adjacent equal sides."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["circle", "circles", "circumference", "radius", "diameter", "pi"],
        "response": (
            "A circle is a round shape where all points are the same distance from the centre. "
            "The radius is the distance from the centre to any point on the circle. The diameter is the distance across the circle through the centre. "
            "The diameter is twice the radius. "
            "The circumference is the distance around the circle. It is calculated by multiplying the diameter by pi, which is approximately 3.14. "
            "The area of a circle is pi times the radius squared. Pi is a special number that is approximately 3.142."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["perimeter", "area", "surface area"],
        "response": (
            "Perimeter is the total distance around the outside of a shape. To find the perimeter, add up the lengths of all the sides. "
            "Area is the amount of space inside a shape. For a rectangle, area equals length times width. "
            "For a triangle, area equals half times base times height. "
            "For a circle, area equals pi times the radius squared. "
            "Surface area is the total area of all the surfaces of a three-dimensional object. "
            "Area is measured in square units like square centimetres or square metres."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["volume", "capacity", "cubic"],
        "response": (
            "Volume is the amount of space inside a three-dimensional object. "
            "For a cuboid or box, volume equals length times width times height. "
            "For a cube where all sides are equal, volume equals side length cubed. "
            "For a cylinder, volume equals pi times the radius squared times the height. "
            "Capacity is the amount a container can hold and is often measured in litres or millilitres. "
            "Volume is measured in cubic units like cubic centimetres or cubic metres."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["symmetry", "line of symmetry", "reflective symmetry", "rotational symmetry"],
        "response": (
            "A shape has reflective symmetry if you can fold it in half so one half matches the other exactly. "
            "The fold line is called the line of symmetry. Some shapes have more than one line of symmetry. "
            "A square has 4 lines of symmetry, a rectangle has 2, and a circle has infinite lines. "
            "Rotational symmetry is when a shape looks the same after being turned around its centre. "
            "The order of rotational symmetry is how many times the shape looks the same in one full turn."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["coordinate", "coordinates", "graph", "axes", "x axis", "y axis", "plot"],
        "response": (
            "Coordinates are used to locate points on a grid. The grid has two axes: the x-axis which runs horizontally, and the y-axis which runs vertically. "
            "A point is written as x comma y in brackets. The x-coordinate tells you how far to move right from zero, and the y-coordinate tells you how far to move up. "
            "For example, the point 3 comma 5 means move 3 steps right and 5 steps up. "
            "The point 0 comma 0 is called the origin. Negative coordinates move left or down."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["scale", "scale drawing", "bearing", "direction"],
        "response": (
            "A scale shows how distance on a map or drawing relates to actual distance. "
            "For example, a scale of 1 to 100 means 1 centimetre on the drawing equals 100 centimetres in real life. "
            "Bearings are used to describe direction. A bearing is an angle measured clockwise from north. It is always written as three digits. "
            "For example, a bearing of 045 degrees means 45 degrees clockwise from north, which is north-east."
        ),
    },

    # ─── Statistics and Probability ───

    {
        "subject": "Mathematics",
        "keywords": ["mean", "median", "mode", "average", "statistics", "range"],
        "response": (
            "Mean, median, mode, and range are ways to describe a set of numbers. "
            "The mean is the sum of all numbers divided by how many numbers there are. For example, the mean of 2, 4, and 6 is 2 plus 4 plus 6 equals 12, divided by 3, which is 4. "
            "The median is the middle number when you arrange the numbers in order from smallest to largest. "
            "If there are two middle numbers, the median is the mean of those two numbers. "
            "The mode is the number that appears most often. "
            "The range is the difference between the largest and smallest numbers."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["probability", "chance", "likely", "unlikely", "certain", "impossible", "outcome"],
        "response": (
            "Probability is the chance that something will happen. It is measured on a scale from 0 to 1. "
            "A probability of 0 means something is impossible. A probability of 1 means something is certain. "
            "For example, when you flip a coin, the probability of getting heads is 1 out of 2, which is 0.5 or 50 percent. "
            "To calculate probability, divide the number of favourable outcomes by the total number of possible outcomes. "
            "For example, when rolling a dice, the probability of rolling a 4 is 1 out of 6."
        ),
    },

    # ─── Measurement ───

    {
        "subject": "Mathematics",
        "keywords": ["measurement", "length", "distance", "millimetre", "centimetre", "metre", "kilometre"],
        "response": (
            "Length measures how long something is. The basic unit of length is the metre. "
            "Smaller units are the centimetre and millimetre. Larger units are the kilometre. "
            "There are 10 millimetres in a centimetre, 100 centimetres in a metre, and 1,000 metres in a kilometre. "
            "To convert from a larger unit to a smaller unit, multiply. To convert from a smaller unit to a larger unit, divide."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["mass", "weight", "gram", "kilogram", "tonne"],
        "response": (
            "Mass is how much matter is in an object. The basic unit of mass is the gram. "
            "There are 1,000 grams in a kilogram, and 1,000 kilograms in a tonne. "
            "To convert kilograms to grams, multiply by 1,000. To convert grams to kilograms, divide by 1,000."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["time", "hour", "minute", "second", "clock", "duration"],
        "response": (
            "Time tells us when events happen and how long they last. The basic units of time are seconds, minutes, hours, days, weeks, months, and years. "
            "There are 60 seconds in a minute, 60 minutes in an hour, and 24 hours in a day. "
            "There are 7 days in a week, and approximately 30 days in a month. "
            "To convert hours to minutes, multiply by 60. To convert minutes to seconds, multiply by 60. "
            "To find the duration between two times, subtract the start time from the end time."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["money", "currency", "leone", "cost", "price", "change", "profit", "loss", "simple interest", "discount"],
        "response": (
            "Money is used to buy goods and services. In Sierra Leone, the currency is the Leone. "
            "To find the total cost, multiply the price by the quantity. To find change, subtract the cost from the amount paid. "
            "Profit equals selling price minus cost price. Loss equals cost price minus selling price. "
            "Discount is a reduction in price, often given as a percentage. "
            "Simple interest is calculated as principal times rate times time divided by 100. "
            "For example, a 5 percent interest on 1,000 Leones for 2 years is 1,000 times 5 times 2 divided by 100, which equals 100 Leones."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["speed", "distance", "time", "average speed"],
        "response": (
            "Speed tells us how fast something is moving. The formula is speed equals distance divided by time. "
            "For example, if you travel 100 kilometres in 2 hours, your average speed is 100 divided by 2, which is 50 kilometres per hour. "
            "To find distance, multiply speed by time. To find time, divide distance by speed. "
            "Average speed accounts for changes in speed during a journey."
        ),
    },
    {
        "subject": "Mathematics",
        "keywords": ["set", "sets", "union", "intersection", "subset", "universal", "empty set"],
        "response": (
            "A set is a collection of distinct objects or numbers. For example, the set of even numbers less than 10 is 2, 4, 6, 8. "
            "The universal set contains everything we are considering. The empty set has no elements. "
            "The union of two sets contains all elements from both sets. The intersection contains only the elements that are in both sets. "
            "A subset is a set where every element is also in another set. "
            "Venn diagrams are used to show relationships between sets visually."
        ),
    },

# ╔══════════════════════════════════════════════════════════════╗
# ║                    SUBJECT: SCIENCE                          ║
# ╚══════════════════════════════════════════════════════════════╝

    # ─── Living Things and Classification ───

    {
        "subject": "Science",
        "keywords": ["living", "non living", "living things", "characteristics of living things"],
        "response": (
            "Living things share seven characteristics. They move, respire, sense their environment, grow, reproduce, excrete waste, and need nutrition. "
            "You can remember these with the word Mrs Gren: Movement, Respiration, Sensitivity, Growth, Reproduction, Excretion, and Nutrition. "
            "Non-living things do not have all these characteristics. For example, a rock does not grow, move, or reproduce. "
            "Some things like seeds appear non-living but will grow into living plants when conditions are right."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["classification", "classify", "kingdom", "species", "vertebrate", "invertebrate"],
        "response": (
            "Classification is sorting living things into groups based on their similarities. The main groups are called kingdoms: animals, plants, fungi, and microorganisms. "
            "Animals are divided into vertebrates, which have a backbone, and invertebrates, which do not. "
            "Vertebrates include mammals, birds, reptiles, amphibians, and fish. "
            "Mammals have hair or fur, give birth to live young, and feed their babies milk. Examples include humans, dogs, and elephants. "
            "Birds have feathers, lay eggs, and have wings. Reptiles have scaly skin and lay eggs on land. "
            "Amphibians live both in water and on land, and have smooth moist skin. Fish live in water, have gills, and lay eggs."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["mammal", "mammals"],
        "response": (
            "Mammals are a group of animals that have hair or fur on their bodies. All mammals are warm-blooded, which means their body temperature stays constant. "
            "Female mammals produce milk to feed their babies. Most mammals give birth to live young rather than laying eggs. "
            "Examples of mammals include humans, dogs, cats, elephants, whales, and bats. "
            "Whales and dolphins are mammals that live in water but breathe air through lungs."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["bird", "birds"],
        "response": (
            "Birds are animals that have feathers, wings, and a beak or bill. They are warm-blooded and lay eggs with hard shells. "
            "Birds have a lightweight skeleton with hollow bones to help them fly. Their wings are shaped to provide lift. "
            "Not all birds can fly. Examples of flightless birds include ostriches, penguins, and emus. "
            "Birds have excellent eyesight and a sharp beak adapted to their diet. For example, eagles have hooked beaks for tearing meat, while hummingbirds have long thin beaks for sipping nectar."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["reptile", "reptiles", "snake", "lizard", "crocodile", "turtle"],
        "response": (
            "Reptiles are cold-blooded animals with dry, scaly skin. They lay eggs on land, and the eggs have leathery shells. "
            "Examples include snakes, lizards, crocodiles, turtles, and tortoises. "
            "Being cold-blooded means their body temperature changes with the environment. They bask in the sun to warm up and hide in shade to cool down. "
            "Snakes have no legs and move by slithering. Some snakes are venomous and use poison to catch prey."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["amphibian", "amphibians", "frog", "toad", "salamander"],
        "response": (
            "Amphibians are cold-blooded animals that live both in water and on land. They have smooth, moist skin. "
            "Frogs and toads are common amphibians. Amphibians lay eggs without shells in water. "
            "The young, called tadpoles, live in water and breathe through gills. As they grow, they develop legs and lungs and move onto land. "
            "This change from a juvenile to an adult form is called metamorphosis."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["fish", "fishes"],
        "response": (
            "Fish are cold-blooded animals that live in water. They have gills to breathe underwater, fins to swim, and scales to protect their bodies. "
            "Most fish lay eggs, but some like sharks give birth to live young. "
            "Fish live in all kinds of water, from rivers and lakes to oceans and seas. "
            "Examples include tilapia, salmon, tuna, and catfish."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["plant", "plants", "flowering plant", "non flowering"],
        "response": (
            "Plants are living things that make their own food through photosynthesis. They are essential for life on Earth because they produce oxygen. "
            "Plants have roots that anchor them in the soil and absorb water and minerals. The stem supports the plant and transports water and nutrients. "
            "Leaves are where photosynthesis happens. "
            "Flowering plants reproduce by making flowers, which develop into fruits containing seeds. "
            "Non-flowering plants like ferns and mosses reproduce using spores instead of seeds."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["flower", "flowers", "part of a flower", "pollination", "fertilisation"],
        "response": (
            "A flower is the reproductive part of a flowering plant. The main parts are the petals, which attract insects, the sepals which protect the bud, "
            "the male part called the stamen which produces pollen, and the female part called the carpel which contains the ovary. "
            "Pollination is when pollen moves from the stamen to the carpel. This can happen by wind or by insects like bees and butterflies. "
            "After pollination, fertilisation occurs and the ovary develops into a fruit containing seeds. "
            "The seeds can grow into new plants through germination."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["seed", "seeds", "germination", "dispersal"],
        "response": (
            "A seed contains a tiny plant inside it, along with a food store to help it start growing. "
            "Germination is when a seed starts to grow into a new plant. It needs water, oxygen, and the right temperature. "
            "First, the root grows downward to anchor the plant and absorb water. Then the shoot grows upward toward the light. "
            "Seed dispersal is how seeds move away from the parent plant so they have space to grow. "
            "Seeds can be dispersed by wind, water, animals, or by exploding pods."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["photosynthesis"],
        "response": (
            "Photosynthesis is the process plants use to make their own food using sunlight. "
            "Plants take in water from the soil through their roots and carbon dioxide from the air through tiny holes in their leaves called stomata. "
            "Using energy from sunlight and a green pigment called chlorophyll, the plant converts water and carbon dioxide into glucose, which is a type of sugar the plant uses for energy. "
            "Oxygen is released as a by-product. The word equation is carbon dioxide plus water plus sunlight makes glucose and oxygen. "
            "Photosynthesis happens in the leaves, in special structures called chloroplasts."
        ),
    },

    # ─── Cells and Human Body ───

    {
        "subject": "Science",
        "keywords": ["cell", "cells", "cell structure", "organelle"],
        "response": (
            "The cell is the basic building block of all living things. Every living organism is made up of cells. "
            "Some organisms have only one cell, called unicellular, like bacteria. Others, like humans, have trillions of cells and are called multicellular. "
            "An animal cell has a cell membrane which controls what enters and leaves the cell, a nucleus which contains DNA and controls the cell, "
            "and cytoplasm where chemical reactions happen. "
            "A plant cell has these parts plus a cell wall for support, a large vacuole for storing water, and chloroplasts for photosynthesis."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["mitosis", "meiosis", "cell division", "chromosome"],
        "response": (
            "Mitosis and meiosis are two types of cell division. "
            "Mitosis produces two identical daughter cells, each with the same number of chromosomes as the parent. It is used for growth and repair. "
            "Meiosis produces four daughter cells, each with half the number of chromosomes. It is used to make sex cells: eggs in females and sperm in males. "
            "When an egg and sperm join during fertilisation, they create a new cell with the full number of chromosomes."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["tissue", "organ", "organ system", "organism"],
        "response": (
            "In multicellular organisms, cells work together in groups. "
            "A tissue is a group of similar cells that do the same job, like muscle tissue or nerve tissue. "
            "An organ is made of different tissues working together, like the heart, lungs, or stomach. "
            "An organ system is a group of organs that work together, like the digestive system or respiratory system. "
            "An organism is a complete living thing made up of many organ systems working together."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["skeleton", "skeletal", "bone", "bones", "joint"],
        "response": (
            "The skeleton is the framework of bones that supports the body and protects internal organs. An adult human has 206 bones. "
            "The skull protects the brain. The rib cage protects the heart and lungs. The spine, or backbone, supports the body and allows movement. "
            "Joints are where two bones meet. Different joints allow different types of movement. "
            "Hinge joints, like the knee and elbow, allow movement in one direction. Ball and socket joints, like the hip and shoulder, allow movement in many directions."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["muscle", "muscles", "voluntary", "involuntary"],
        "response": (
            "Muscles help the body move by contracting and relaxing. There are three types of muscles. "
            "Skeletal muscles are attached to bones and are voluntary, meaning you control them. They help you walk, run, and lift things. "
            "Smooth muscles are found in organs like the stomach and intestines. They are involuntary, meaning they work without you thinking about them. "
            "Cardiac muscle is found only in the heart. It works non-stop without you thinking about it."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["digestion", "digestive system", "digest", "digestive"],
        "response": (
            "The digestive system breaks down food into nutrients that the body can use for energy, growth, and repair. "
            "Digestion begins in the mouth where teeth chew food and saliva starts to break it down. "
            "The food travels down the oesophagus to the stomach, where strong digestive juices break it down further. "
            "Next, it moves to the small intestine, where nutrients are absorbed into the bloodstream. "
            "The large intestine absorbs water, and the remaining waste leaves the body. The process takes about 24 to 48 hours."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["respiratory", "respiration", "breathing", "breathe", "lungs", "trachea", "diaphragm"],
        "response": (
            "Respiration is how the body takes in oxygen and removes carbon dioxide. "
            "When you breathe in, air enters through your nose or mouth and travels down the trachea, or windpipe, into the lungs. "
            "In the lungs, tiny air sacs called alveoli transfer oxygen into the blood and remove carbon dioxide from it. "
            "The diaphragm is a large muscle below the lungs that helps you breathe. When it contracts, you inhale, and when it relaxes, you exhale. "
            "Cellular respiration is different from breathing. It is the process inside cells that uses oxygen to release energy from glucose."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["circulatory", "heart", "blood", "blood vessel", "artery", "vein", "capillary"],
        "response": (
            "The circulatory system transports blood around the body. The heart is a muscular pump that pushes blood through blood vessels. "
            "Arteries carry blood away from the heart to the rest of the body. They have thick walls because blood is under pressure. "
            "Veins carry blood back to the heart. They have valves to stop blood flowing backward. "
            "Capillaries are tiny blood vessels where oxygen and nutrients pass from the blood into cells. "
            "Blood carries oxygen, nutrients, hormones, and waste products. It also helps fight infections."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["nervous system", "brain", "nerve", "neuron", "spinal cord", "reflex"],
        "response": (
            "The nervous system controls and coordinates all body activities. It has two main parts: the central nervous system and the peripheral nervous system. "
            "The central nervous system consists of the brain and spinal cord. The brain controls thoughts, memories, and movements. "
            "The peripheral nervous system consists of nerves that connect the brain and spinal cord to the rest of the body. "
            "Neurons are nerve cells that carry electrical signals. A reflex is a quick automatic response that does not involve the brain, like pulling your hand away from something hot."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["sense", "senses", "sight", "hearing", "touch", "taste", "smell", "sensory"],
        "response": (
            "The five senses help us understand the world around us. "
            "Sight uses the eyes to detect light. Hearing uses the ears to detect sound. "
            "Touch uses the skin to feel pressure, temperature, and pain. "
            "Taste uses the tongue to detect sweet, sour, salty, bitter, and umami flavours. "
            "Smell uses the nose to detect odours. The senses work together to give us a complete picture of our environment."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["nutrition", "diet", "food", "nutrient", "carbohydrate", "protein", "fat", "vitamin", "mineral", "fibre"],
        "response": (
            "Nutrition is about the food we eat and how our body uses it. A balanced diet includes all the nutrients the body needs. "
            "Carbohydrates provide energy. They are found in rice, bread, and cassava. "
            "Proteins help the body grow and repair itself. They are found in meat, fish, eggs, and beans. "
            "Fats provide energy and help absorb vitamins. They are found in oil, butter, and nuts. "
            "Vitamins and minerals are needed in small amounts for various body functions. For example, vitamin C helps prevent illness, and calcium is needed for strong bones. "
            "Fibre helps digestion and is found in fruits, vegetables, and whole grains. Water is also essential for life."
        ),
    },

    # ─── Ecosystems ───

    {
        "subject": "Science",
        "keywords": ["ecosystem", "ecology", "habitat", "environment"],
        "response": (
            "An ecosystem is a community of living things interacting with each other and their physical environment. "
            "A habitat is the natural home of a plant or animal. For example, a pond is a habitat for frogs and water lilies. "
            "In an ecosystem, living things depend on each other for food, shelter, and other needs. "
            "The physical environment includes sunlight, temperature, water, and soil. "
            "Changes to one part of an ecosystem can affect the whole system."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["food chain", "food web", "producer", "consumer", "decomposer", "herbivore", "carnivore", "omnivore"],
        "response": (
            "A food chain shows how energy passes from one living thing to another. It always starts with a producer, which is a plant that makes its own food. "
            "The next link is a primary consumer that eats the plant. This is a herbivore, an animal that eats only plants. "
            "Next is a secondary consumer that eats the herbivore. This is a carnivore, an animal that eats other animals. "
            "Omnivores eat both plants and animals. "
            "A food web is a network of connected food chains. "
            "Decomposers, like bacteria and fungi, break down dead organisms and return nutrients to the soil."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["adaptation", "adapt", "camouflage"],
        "response": (
            "Adaptation is how a living thing changes over time to survive better in its environment. "
            "For example, cacti have thick stems to store water in dry deserts. "
            "Camouflage is an adaptation where an animal's colour or pattern helps it blend into its surroundings to hide from predators or sneak up on prey. "
            "Other adaptations include sharp teeth for eating meat, long necks for reaching high leaves, and webbed feet for swimming."
        ),
    },

    # ─── Materials and Matter ───

    {
        "subject": "Science",
        "keywords": ["material", "materials", "property", "properties", "hard", "soft", "flexible", "waterproof", "transparent"],
        "response": (
            "Materials are what things are made from. Different materials have different properties, which make them suitable for different uses. "
            "Hard materials like metal are difficult to scratch. Soft materials like fabric are easy to shape. "
            "Flexible materials like rubber can bend without breaking. Waterproof materials like plastic do not let water through. "
            "Transparent materials like glass let light pass through so you can see through them. "
            "Choosing the right material for a job depends on its properties."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["solid", "liquid", "gas", "states of matter", "state of matter", "melting", "freezing", "boiling", "evaporation", "condensation"],
        "response": (
            "Everything is made of matter, which exists in three main states: solid, liquid, and gas. "
            "In a solid, particles are packed tightly together and can only vibrate. Solids have a fixed shape and volume. "
            "In a liquid, particles are close but can move past each other. Liquids have a fixed volume but take the shape of their container. "
            "In a gas, particles are far apart and move quickly. Gases have no fixed shape or volume. "
            "Melting is when a solid turns into a liquid. Freezing is when a liquid turns into a solid. "
            "Boiling and evaporation turn a liquid into a gas. Condensation turns a gas into a liquid."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["atom", "atoms", "molecule", "molecules", "element", "compound", "mixture"],
        "response": (
            "An atom is the smallest particle of an element. Everything around us is made of atoms. "
            "An element is a substance made of only one type of atom. Examples include oxygen, iron, gold, and carbon. There are over 100 known elements. "
            "A molecule is formed when two or more atoms join together. For example, a water molecule has two hydrogen atoms and one oxygen atom. "
            "A compound is a substance made of different elements chemically joined. For example, salt is a compound of sodium and chlorine. "
            "A mixture is made of different substances mixed together but not chemically joined, like sand and water."
        ),
    },

    # ─── Forces and Energy ───

    {
        "subject": "Science",
        "keywords": ["force", "forces", "push", "pull"],
        "response": (
            "A force is a push or pull that can make an object move, stop, change speed, change direction, or change shape. "
            "Forces are measured in newtons using a device called a force meter or spring balance. "
            "Examples of forces include gravity, which pulls things toward Earth, friction, which slows moving objects, "
            "and magnetic force, which pulls or pushes magnetic materials."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["friction", "air resistance", "water resistance", "drag"],
        "response": (
            "Friction is a force that opposes motion when two surfaces rub against each other. It slows things down and produces heat. "
            "Rough surfaces create more friction than smooth surfaces. That is why soles of shoes have treads to increase friction and prevent slipping. "
            "Air resistance, also called drag, is a type of friction that acts on objects moving through air. "
            "Water resistance is friction that acts on objects moving through water. Streamlined shapes reduce water and air resistance."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["gravity", "gravitational", "weight", "mass"],
        "response": (
            "Gravity is a force that pulls objects with mass toward each other. The Earth's gravity pulls everything toward the centre of the planet. "
            "Mass is the amount of matter in an object and is measured in kilograms. Weight is the force of gravity acting on an object and is measured in newtons. "
            "Your mass stays the same anywhere in the universe, but your weight changes depending on the strength of gravity. "
            "On the Moon, gravity is about 6 times weaker, so you would weigh much less. The force of gravity on Earth is approximately 9.8 metres per second squared."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["energy", "energy transfer", "kinetic", "potential", "heat", "light", "sound", "electrical", "chemical"],
        "response": (
            "Energy is the ability to do work or cause change. It cannot be created or destroyed, only transferred from one form to another. "
            "Kinetic energy is the energy of moving objects. Potential energy is stored energy, like a ball at the top of a hill. "
            "Heat or thermal energy is the energy of moving particles. Light energy comes from sources like the Sun and light bulbs. "
            "Sound energy is produced by vibrating objects. Electrical energy is the flow of electric charge. "
            "Chemical energy is stored in food, batteries, and fuel. The law of conservation of energy says energy cannot be created or destroyed, only changed."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["sound", "vibration", "pitch", "volume", "echo"],
        "response": (
            "Sound is produced when objects vibrate. The vibrations travel through the air as sound waves and reach our ears. "
            "Sound can travel through solids, liquids, and gases, but cannot travel through empty space. "
            "Pitch is how high or low a sound is. A high pitch is produced by fast vibrations, like a whistle. A low pitch is produced by slow vibrations, like a drum. "
            "Volume is how loud or quiet a sound is. Larger vibrations produce louder sounds. "
            "An echo is a reflected sound wave. You hear an echo when sound bounces off a hard surface and comes back to you."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["light", "light source", "shadow", "reflection", "refraction"],
        "response": (
            "Light is a form of energy that allows us to see. It travels in straight lines at very high speed. "
            "Light sources, like the Sun, stars, and light bulbs, produce their own light. The Moon is not a light source; it reflects the Sun's light. "
            "Shadows form when an object blocks light. The shape of the shadow depends on the position of the light source. "
            "Reflection is when light bounces off a surface. Mirrors reflect light well, which is why we can see our reflection in them. "
            "Refraction is when light bends as it passes from one material to another, like from air to water."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["electricity", "electric", "current", "circuit", "battery", "cell", "bulb"],
        "response": (
            "Electricity is a form of energy that flows through wires. An electric current is the flow of tiny charged particles called electrons. "
            "A circuit is a complete path that electricity can flow around. It needs a power source like a battery, wires to carry the current, and a device like a bulb to use the energy. "
            "If the circuit is broken, the current stops flowing and the device will not work. This is why switches are used to turn things on and off. "
            "Conductors, like copper and aluminium, allow electricity to flow through them easily. Insulators, like plastic and rubber, do not."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["magnet", "magnetism", "magnetic", "pole", "attract", "repel"],
        "response": (
            "Magnetism is a force that can attract or repel certain materials. Only magnetic materials are affected, like iron, steel, nickel, and cobalt. "
            "A magnet has two ends called poles: a north pole and a south pole. Opposite poles attract each other, while the same poles repel each other. "
            "The Earth itself acts like a giant magnet, which is why a compass needle always points north. "
            "Magnets are used in speakers, electric motors, door catches, and credit card strips."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["machine", "simple machine", "lever", "pulley", "inclined plane", "screw", "wheel", "axle", "wedge"],
        "response": (
            "Simple machines make work easier by changing the size or direction of a force. "
            "A lever is a bar that pivots on a point called a fulcrum. Examples include seesaws and crowbars. "
            "A pulley uses a wheel and a rope to lift heavy objects. "
            "An inclined plane, or ramp, makes it easier to move objects from a lower to a higher level. "
            "A screw is an inclined plane wrapped around a cylinder. A wedge is used to split things apart, like an axe. "
            "A wheel and axle makes moving things easier, like on a cart or bicycle."
        ),
    },

    # ─── Earth and Space ───

    {
        "subject": "Science",
        "keywords": ["solar system", "planet", "sun", "orbit", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"],
        "response": (
            "Our solar system consists of the Sun and everything that orbits around it, including eight planets. "
            "The planets in order from the Sun are Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. "
            "Mercury is the smallest and closest to the Sun. Venus is the hottest planet. "
            "Earth is the third planet and the only one known to support life. Mars is called the red planet. "
            "Jupiter is the largest planet. Saturn is known for its beautiful rings. "
            "Uranus and Neptune are the furthest and coldest planets."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["earth", "day and night", "rotation", "axis"],
        "response": (
            "The Earth rotates on its axis, an imaginary line through the North and South Poles. "
            "One complete rotation takes 24 hours, which is why we have day and night. "
            "The side of Earth facing the Sun experiences daytime, while the side facing away experiences night. "
            "Earth also orbits the Sun, and one complete orbit takes about 365 days, which is one year. "
            "The Earth's axis is tilted, which causes the seasons."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["moon", "moon phase", "crescent", "gibbous", "new moon", "full moon"],
        "response": (
            "The Moon is Earth's only natural satellite. It orbits Earth about once every 28 days. "
            "The Moon does not produce its own light; we see it because it reflects sunlight. "
            "As the Moon orbits Earth, we see different amounts of the lit side. These are called moon phases. "
            "The main phases are new moon, crescent, first quarter, gibbous, full moon, and then back through gibbous, last quarter, and crescent."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["rock", "rocks", "mineral", "igneous", "sedimentary", "metamorphic", "volcano", "earthquake"],
        "response": (
            "Rocks are made of minerals. There are three main types of rock. "
            "Igneous rocks form when molten magma from inside the Earth cools and solidifies. Examples include granite and basalt. "
            "Sedimentary rocks form when layers of sand, mud, or shells are pressed together over millions of years. Examples include limestone and sandstone. "
            "Metamorphic rocks form when existing rocks are changed by heat and pressure. Examples include marble and slate. "
            "A volcano is an opening in the Earth's surface where molten rock, ash, and gases erupt. "
            "An earthquake is a sudden shaking of the ground caused by movement of tectonic plates beneath the Earth's surface."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["water cycle", "evaporation", "condensation", "precipitation", "collection"],
        "response": (
            "The water cycle is the continuous movement of water on Earth. It has four main stages. "
            "First, evaporation occurs when the Sun heats water in rivers, lakes, and oceans, turning it into water vapour. "
            "Second, transpiration is when water evaporates from plant leaves. "
            "Third, condensation happens when water vapour cools high in the sky and turns back into tiny water droplets, forming clouds. "
            "Fourth, precipitation occurs when the droplets become heavy and fall as rain, snow, or hail. "
            "Finally, collection is when the water gathers in rivers, lakes, and oceans, and the cycle starts again."
        ),
    },
    {
        "subject": "Science",
        "keywords": ["weather", "climate", "rainfall", "temperature", "wind", "season"],
        "response": (
            "Weather is the condition of the atmosphere at a particular time and place, including temperature, rainfall, wind, and cloud cover. "
            "Climate is the average weather pattern of a place over many years. "
            "Temperature is measured with a thermometer in degrees Celsius. Rainfall is measured with a rain gauge. "
            "Wind speed is measured with an anemometer, and wind direction is shown by a wind vane. "
            "Sierra Leone has a tropical climate with two main seasons: the rainy season from May to October and the dry season from November to April."
        ),
    },

# ╔══════════════════════════════════════════════════════════════╗
# ║                    SUBJECT: ENGLISH                          ║
# ╚══════════════════════════════════════════════════════════════╝

    # ─── Parts of Speech ───

    {
        "subject": "English",
        "keywords": ["noun", "nouns", "common noun", "proper noun", "abstract noun", "collective noun"],
        "response": (
            "A noun is a word that names a person, place, thing, or idea. "
            "Common nouns name general things, like city, teacher, or book. They start with a small letter. "
            "Proper nouns name specific things, like Freetown, Mr Kamara, or Sierra Leone. They always start with a capital letter. "
            "Abstract nouns name ideas or feelings that you cannot touch, like love, happiness, or courage. "
            "Collective nouns name a group, like a team of players, a flock of birds, or a crowd of people."
        ),
    },
    {
        "subject": "English",
        "keywords": ["verb", "verbs", "action verb", "linking verb", "auxiliary", "modal"],
        "response": (
            "A verb is a word that describes an action, occurrence, or state of being. "
            "Action verbs describe physical or mental actions, like run, eat, think, or write. "
            "Linking verbs connect the subject to more information, like is, are, was, and were. For example, she is a teacher. "
            "Auxiliary verbs, also called helping verbs, help the main verb. They include be, have, and do. "
            "Modal verbs express possibility or necessity, like can, must, should, and will."
        ),
    },
    {
        "subject": "English",
        "keywords": ["adjective", "adjectives", "comparative", "superlative"],
        "response": (
            "An adjective is a word that describes a noun. It tells us more about a person, place, or thing. "
            "For example, in the tall building, the word tall is an adjective. Other examples are beautiful, happy, big, small, bright, and dark. "
            "Comparative adjectives compare two things and usually end in E R, like taller or bigger. Sometimes we use more, like more beautiful. "
            "Superlative adjectives compare three or more things and usually end in E S T, like tallest or biggest. Sometimes we use most, like most beautiful."
        ),
    },
    {
        "subject": "English",
        "keywords": ["adverb", "adverbs", "manner", "time", "place", "frequency"],
        "response": (
            "An adverb is a word that describes a verb, an adjective, or another adverb. It often tells how, when, where, or how often something happens. "
            "Adverbs of manner describe how something happens, like quickly, slowly, or carefully. "
            "Adverbs of time tell when something happens, like now, later, yesterday, or soon. "
            "Adverbs of place tell where something happens, like here, there, everywhere, or inside. "
            "Adverbs of frequency tell how often something happens, like always, sometimes, never, or often."
        ),
    },
    {
        "subject": "English",
        "keywords": ["pronoun", "pronouns", "personal", "possessive", "reflexive", "demonstrative"],
        "response": (
            "A pronoun takes the place of a noun to avoid repeating it. "
            "Personal pronouns include I, you, he, she, it, we, and they. Object pronouns include me, him, her, us, and them. "
            "Possessive pronouns show ownership: my, your, his, her, its, our, their. "
            "Reflexive pronouns refer back to the subject: myself, yourself, himself, herself, itself, ourselves, themselves. "
            "Demonstrative pronouns point to specific things: this, that, these, those."
        ),
    },
    {
        "subject": "English",
        "keywords": ["preposition", "prepositions", "position", "direction", "time"],
        "response": (
            "A preposition shows the relationship between a noun or pronoun and other words in the sentence. "
            "Prepositions of position include in, on, at, under, over, between, beside, behind, and in front of. "
            "Prepositions of direction include to, towards, into, through, across, and along. "
            "Prepositions of time include before, after, during, since, until, and at. "
            "For example, in the book is on the table, the word on shows the relationship between the book and the table."
        ),
    },
    {
        "subject": "English",
        "keywords": ["conjunction", "conjunctions", "connective", "coordinating", "subordinating"],
        "response": (
            "A conjunction connects words, phrases, or clauses. "
            "Coordinating conjunctions join equal parts of a sentence. They are for, and, nor, but, or, yet, so. You can remember them as FANBOYS. "
            "Subordinating conjunctions join a main clause and a subordinate clause. Examples include because, although, while, if, when, since, and unless. "
            "For example, in I stayed home because it was raining, the word because is a subordinating conjunction."
        ),
    },
    {
        "subject": "English",
        "keywords": ["interjection", "interjections"],
        "response": (
            "An interjection is a word or phrase that expresses strong emotion. It is often followed by an exclamation mark. "
            "Examples include Wow, Oh no, Ouch, Hurray, Alas, and Oh dear. "
            "Interjections are not grammatically connected to the rest of the sentence. "
            "For example: Wow, that is amazing. Or Ouch, I hurt my finger."
        ),
    },

    # ─── Tenses ───

    {
        "subject": "English",
        "keywords": ["present tense", "simple present"],
        "response": (
            "The simple present tense describes actions that happen regularly, habits, or general truths. "
            "For example, I walk to school every day, or the Sun rises in the east. "
            "For he, she, and it, add an S to the verb, like he walks or she runs. "
            "To form negatives, use do not or does not: I do not like spiders, or she does not eat meat. "
            "To form questions, use do or does: Do you like music, or does he play football."
        ),
    },
    {
        "subject": "English",
        "keywords": ["present continuous", "present progressive"],
        "response": (
            "The present continuous tense describes actions happening right now or around now. "
            "It is formed using am, is, or are plus the verb ending in I N G. "
            "For example, I am reading a book, she is cooking dinner, or they are playing football. "
            "To form negatives, add not: I am not sleeping, or he is not working. "
            "To form questions, move am, is, or are to the beginning: Are you coming?"
        ),
    },
    {
        "subject": "English",
        "keywords": ["past tense", "simple past", "regular verb", "irregular verb"],
        "response": (
            "The simple past tense describes actions that already happened. "
            "Regular verbs form the past tense by adding E D, like walk becomes walked, or play becomes played. "
            "Irregular verbs change form completely, like go becomes went, eat becomes ate, and buy becomes bought. "
            "You need to learn the past forms of irregular verbs because they do not follow a rule. "
            "To form negatives, use did not: I did not go, or she did not come."
        ),
    },
    {
        "subject": "English",
        "keywords": ["past continuous", "past progressive"],
        "response": (
            "The past continuous tense describes actions that were in progress at a specific time in the past. "
            "It is formed using was or were plus the verb ending in I N G. "
            "For example, I was reading when you called, or they were playing football at 4 o'clock. "
            "It is often used with the simple past to show a longer action interrupted by a shorter action."
        ),
    },
    {
        "subject": "English",
        "keywords": ["future tense", "simple future", "going to"],
        "response": (
            "The simple future tense describes actions that will happen later. "
            "It can be formed using will plus the verb, like I will go to school tomorrow. "
            "It can also be formed using going to: I am going to visit my grandmother. "
            "For negatives, use will not or won't: I will not come, or she won't be there. "
            "For questions, move will to the beginning: Will you help me?"
        ),
    },
    {
        "subject": "English",
        "keywords": ["present perfect"],
        "response": (
            "The present perfect tense connects the past to the present. It is formed using have or has plus the past participle of the verb. "
            "For example, I have finished my homework, or she has visited Freetown. "
            "It is used for actions that happened at an unspecified time in the past, or actions that started in the past and continue to now. "
            "For negatives, use have not or has not: I have not seen that movie."
        ),
    },

    # ─── Sentence Structure ───

    {
        "subject": "English",
        "keywords": ["sentence", "sentences", "subject", "predicate", "clause"],
        "response": (
            "A sentence is a group of words that expresses a complete thought. It begins with a capital letter and ends with a full stop, question mark, or exclamation mark. "
            "Every sentence has a subject and a predicate. The subject is who or what the sentence is about. The predicate tells what the subject does or is. "
            "For example, in the boy runs fast, the boy is the subject and runs fast is the predicate. "
            "A clause is a group of words with a subject and a verb. An independent clause can stand alone as a sentence. "
            "A dependent clause cannot stand alone and needs an independent clause to complete its meaning."
        ),
    },
    {
        "subject": "English",
        "keywords": ["simple sentence", "compound sentence", "complex sentence"],
        "response": (
            "There are three main types of sentences. "
            "A simple sentence has one independent clause, like I like cats. "
            "A compound sentence has two independent clauses joined by a conjunction, like I like cats but I do not like dogs. "
            "A complex sentence has one independent clause and one or more dependent clauses, like I like cats because they are friendly."
        ),
    },
    {
        "subject": "English",
        "keywords": ["statement", "question", "command", "exclamation", "sentence types", "declarative", "interrogative", "imperative", "exclamatory"],
        "response": (
            "There are four types of sentences based on function. "
            "A statement or declarative sentence gives information and ends with a full stop, like I am a student. "
            "A question or interrogative sentence asks something and ends with a question mark, like What is your name. "
            "A command or imperative sentence gives an order and ends with a full stop or exclamation mark, like Sit down. "
            "An exclamation or exclamatory sentence expresses strong emotion and ends with an exclamation mark, like What a beautiful day."
        ),
    },

    # ─── Punctuation ───

    {
        "subject": "English",
        "keywords": ["punctuation", "full stop", "comma", "question mark", "exclamation mark", "apostrophe", "quotation mark", "colon", "semicolon"],
        "response": (
            "Punctuation marks help make writing clear and easy to read. "
            "A full stop or period ends a sentence. A question mark ends a question. An exclamation mark shows strong feeling. "
            "A comma separates items in a list, like I bought apples, oranges, and bananas. It also adds a pause in a sentence. "
            "An apostrophe shows ownership, like Sarah's book, or missing letters in contractions like don't for do not. "
            "Quotation marks enclose spoken words: She said, I am happy. "
            "A colon introduces a list or explanation. A semicolon connects two related sentences."
        ),
    },
    {
        "subject": "English",
        "keywords": ["capital letter", "capitalisation", "capitalization"],
        "response": (
            "Capital letters are used at the beginning of a sentence, for proper nouns, and for the pronoun I. "
            "Proper nouns include names of people, like Abdul, places, like Freetown, days of the week, like Monday, months, like January, and nationalities, like Sierra Leonean. "
            "Titles of books, films, and songs also use capital letters for the main words."
        ),
    },

    # ─── Writing ───

    {
        "subject": "English",
        "keywords": ["paragraph", "paragraphs", "topic sentence", "supporting sentence", "concluding sentence"],
        "response": (
            "A paragraph is a group of sentences about one main idea. It usually starts on a new line. "
            "The topic sentence introduces the main idea of the paragraph. It is often the first sentence. "
            "Supporting sentences give more details, examples, or explanations about the topic sentence. "
            "The concluding sentence sums up the paragraph or leads to the next one. "
            "When writing an essay, use paragraphs to organize your ideas clearly."
        ),
    },
    {
        "subject": "English",
        "keywords": ["essay", "essay writing", "introduction", "body", "conclusion"],
        "response": (
            "An essay has three main parts: introduction, body, and conclusion. "
            "The introduction introduces the topic and presents the main idea or thesis statement. "
            "The body contains several paragraphs, each covering one main point with supporting details and examples. "
            "The conclusion summarizes the main points and gives a final thought. "
            "Before writing, plan your essay by brainstorming ideas and organizing them into an outline."
        ),
    },
    {
        "subject": "English",
        "keywords": ["letter", "letter writing", "formal letter", "informal letter", "friendly letter"],
        "response": (
            "A letter can be formal or informal. Formal letters are written to people you do not know well, like officials or companies. "
            "A formal letter includes your address, the date, the recipient's address, a formal greeting like Dear Sir or Madam, "
            "a clear subject line, the body of the letter, a formal closing like Yours faithfully, and your signature. "
            "Informal letters are written to friends and family. They include your address, the date, a friendly greeting like Dear Mama, "
            "the body, and a friendly closing like Your loving son, followed by your name."
        ),
    },
    {
        "subject": "English",
        "keywords": ["summary", "summarize", "summarising", "main idea"],
        "response": (
            "A summary is a short version of a longer text that includes only the most important points. "
            "To write a good summary, first read the text carefully and identify the main idea. "
            "Then pick out the key supporting points and leave out minor details and examples. "
            "Write the summary in your own words, keeping it brief and clear. "
            "A good summary is usually about one quarter to one third the length of the original text."
        ),
    },
    {
        "subject": "English",
        "keywords": ["narrative", "narrative writing", "story", "story writing"],
        "response": (
            "Narrative writing tells a story. It can be real or imaginary. "
            "A good story has a clear beginning, middle, and end. The beginning introduces the characters and setting. "
            "The middle presents a problem or conflict. The end shows how the problem is resolved. "
            "Use descriptive language to make the story interesting. Include details about what characters see, hear, and feel. "
            "Use time words like first, then, after that, and finally to show the order of events."
        ),
    },
    {
        "subject": "English",
        "keywords": ["descriptive", "descriptive writing"],
        "response": (
            "Descriptive writing paints a picture with words. It helps the reader imagine a person, place, or thing. "
            "Use sensory details that describe how something looks, sounds, smells, tastes, and feels. "
            "Use adjectives and adverbs to make descriptions vivid. For example, instead of saying the food was good, say the warm spicy soup tasted delicious. "
            "Organize your description in a logical order, such as from top to bottom or from near to far."
        ),
    },

    # ─── Vocabulary and Spelling ───

    {
        "subject": "English",
        "keywords": ["synonym", "synonyms", "antonym", "antonyms"],
        "response": (
            "Synonyms are words that have similar meanings. For example, big and large are synonyms. Happy and joyful are synonyms. "
            "Antonyms are words that have opposite meanings. For example, hot and cold are antonyms. Up and down are antonyms. "
            "Using synonyms makes your writing more interesting and varied."
        ),
    },
    {
        "subject": "English",
        "keywords": ["prefix", "prefixes", "suffix", "suffixes", "root word"],
        "response": (
            "A prefix is added to the beginning of a root word to change its meaning. "
            "For example, un means not, so unhappy means not happy. Re means again, so rewrite means write again. "
            "A suffix is added to the end of a root word. "
            "For example, less means without, so fearless means without fear. Ful means full of, so helpful means full of help. "
            "Knowing prefixes and suffixes helps you understand new words."
        ),
    },
    {
        "subject": "English",
        "keywords": ["homophone", "homophones", "homonym", "homonyms"],
        "response": (
            "Homophones are words that sound the same but have different meanings and spellings. "
            "For example, their, there, and they're sound alike but mean different things. "
            "Their shows ownership: their books. There shows a place: over there. They're means they are. "
            "Other examples include two, to, and too, and write and right."
        ),
    },
    {
        "subject": "English",
        "keywords": ["figure of speech", "simile", "metaphor", "personification", "idiom", "hyperbole"],
        "response": (
            "Figures of speech make language more vivid and interesting. "
            "A simile compares two things using like or as. For example, she is as brave as a lion. "
            "A metaphor compares two things directly without like or as. For example, he is a lion in battle. "
            "Personification gives human qualities to non-human things. For example, the wind whispered through the trees. "
            "An idiom is a phrase with a meaning different from the literal words, like it is raining cats and dogs. "
            "Hyperbole is an extreme exaggeration, like I have told you a million times."
        ),
    },

    # ─── Literature ───

    {
        "subject": "English",
        "keywords": ["poem", "poetry", "poet", "rhyme", "rhythm", "stanza", "verse"],
        "response": (
            "Poetry is a type of writing that uses language in a creative and imaginative way. "
            "A poem is a piece of poetry. The person who writes a poem is called a poet. "
            "Rhyme is when words have the same ending sound, like cat and hat. "
            "Rhythm is the beat or pattern of stressed and unstressed syllables in a poem. "
            "A stanza is a group of lines in a poem, like a paragraph in prose. "
            "Poems often use figures of speech to create vivid images and emotions."
        ),
    },
    {
        "subject": "English",
        "keywords": ["prose", "drama", "play", "dialogue", "character", "plot", "setting", "theme"],
        "response": (
            "Prose is ordinary writing that is not poetry. Novels, short stories, and essays are examples of prose. "
            "Drama is a story written to be performed by actors on a stage. A play is a work of drama. "
            "The plot is the sequence of events in a story. The setting is where and when the story takes place. "
            "Characters are the people or animals in the story. The theme is the main message or lesson. "
            "Dialogue is the conversation between characters, shown with quotation marks."
        ),
    },
    {
        "subject": "English",
        "keywords": ["comprehension", "reading comprehension"],
        "response": (
            "Reading comprehension is understanding what you read. "
            "To improve comprehension, read carefully and think about the main idea of each paragraph. "
            "Look up any words you do not understand. Ask yourself questions about the text, like who, what, where, when, why, and how. "
            "After reading, summarize what you have learned in your own words. "
            "Practice reading different types of texts, such as stories, news articles, and textbooks."
        ),
    },

# ╔══════════════════════════════════════════════════════════════╗
# ║                  SUBJECT: SOCIAL STUDIES                     ║
# ╚══════════════════════════════════════════════════════════════╝

    # ─── Sierra Leone ───

    {
        "subject": "Social Studies",
        "keywords": ["sierra leone", "freetown", "capital of sierra leone"],
        "response": (
            "Sierra Leone is a country on the west coast of Africa. The capital city is Freetown. "
            "Sierra Leone gained independence from Britain on April 27, 1961. "
            "The country is known for its beautiful beaches, diamond mines, and rich cultural traditions. "
            "The main ethnic groups are the Temne and Mende, along with the Limba, Kono, Koranko, and others. "
            "English is the official language, and Krio is widely spoken across the country. "
            "Sierra Leone has five regions: the Western Area and four provinces: the Northern Province, North West Province, Southern Province, and Eastern Province."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["milton margai", "sir milton", "first prime minister", "independence leader"],
        "response": (
            "Sir Milton Margai was a doctor and politician who became the first Prime Minister of Sierra Leone. "
            "He led the country to independence from Britain on April 27, 1961. "
            "He was born in 1895 in Bogo Chiefdom, Moyamba District. He studied medicine in England and returned to Sierra Leone to work as a doctor. "
            "He is remembered as a kind and wise leader who helped unite the country. "
            "The Milton Margai School for the Blind is named after him in honour of his contributions to education."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["siaka stevens", "president", "apc", "all people's congress"],
        "response": (
            "Siaka Stevens was the first President of Sierra Leone, serving from 1971 to 1985. "
            "He was the leader of the All People's Congress party, also known as the APC. "
            "During his presidency, Sierra Leone became a one-party state. "
            "He was succeeded by Joseph Momoh. Stevens is a significant figure in Sierra Leone's political history."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["civil war", "sierra leone civil war", "rebel", "ruf", "peace"],
        "response": (
            "Sierra Leone experienced a devastating civil war from 1991 to 2002. "
            "The war was fought between the government and rebel groups, mainly the Revolutionary United Front or RUF. "
            "The war caused great suffering, with many people killed or displaced. "
            "The war ended in 2002 with the help of international forces, including the United Kingdom and the United Nations. "
            "Since the war, Sierra Leone has worked to rebuild and maintain peace through a democratic government."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["district", "province", "chiefdom", "local government"],
        "response": (
            "Sierra Leone is divided into five regions: the Western Area, Northern Province, North West Province, Southern Province, and Eastern Province. "
            "These regions are divided into 16 districts. Each district has a council that manages local services. "
            "Districts are further divided into chiefdoms, which are traditional administrative units led by paramount chiefs. "
            "Paramount chiefs play an important role in local governance, dispute resolution, and preserving cultural traditions."
        ),
    },

    # ─── Government ───

    {
        "subject": "Social Studies",
        "keywords": ["government", "democracy", "democratic", "constitution"],
        "response": (
            "Sierra Leone is a democratic country. Democracy means that the people have the power to choose their leaders through elections. "
            "The Constitution is the highest law of the land. It sets out the rights and responsibilities of citizens and the structure of government. "
            "The government has three branches: the Executive, the Legislature, and the Judiciary. "
            "This separation of powers ensures that no single branch has too much power."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["executive", "president", "vice president", "cabinet", "minister"],
        "response": (
            "The Executive branch of government is responsible for implementing and enforcing laws. "
            "The President is the head of state and government, elected by the people for a five-year term. "
            "The Vice President assists the President. The President appoints ministers to lead different government departments, like the Minister of Education or Minister of Health. "
            "Together, the President and ministers form the Cabinet, which makes important decisions about running the country."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["legislature", "parliament", "member of parliament", "mp", "speaker"],
        "response": (
            "The Legislature, also called Parliament, is responsible for making laws. "
            "Parliament has two parts: the President and the Members of Parliament, or MPs. "
            "MPs are elected by the people to represent their constituencies. "
            "The Speaker presides over Parliament and ensures that debates are conducted properly. "
            "Before a proposal becomes a law, it must be debated and approved by Parliament, and then signed by the President."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["judiciary", "court", "judge", "supreme court", "legal", "justice"],
        "response": (
            "The Judiciary is the branch of government that interprets laws and administers justice. "
            "It is independent of the Executive and Legislature. The courts hear cases and make decisions based on the law. "
            "The highest court in Sierra Leone is the Supreme Court. Below it are the Court of Appeal, the High Court, and magistrates courts. "
            "Judges are appointed and must be impartial, meaning they do not favour any side. "
            "The rule of law means that everyone, including the government, must follow the law."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["election", "vote", "voting", "electoral", "ballot"],
        "response": (
            "An election is when citizens vote to choose their leaders. In Sierra Leone, elections are held every five years for President and Parliament. "
            "Any citizen who is 18 years or older and registered to vote can participate. "
            "Voting is done by secret ballot, meaning no one else can see who you voted for. "
            "The National Electoral Commission, or NEC, organizes and supervises elections to ensure they are free and fair."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["citizen", "citizenship", "rights", "responsibilities"],
        "response": (
            "A citizen is a legal member of a country with rights and responsibilities. "
            "Rights include the right to life, freedom of speech, freedom of religion, the right to education, and the right to vote. "
            "Responsibilities include obeying the law, paying taxes, respecting others, protecting the environment, and participating in community development. "
            "Good citizens contribute to their community and help make their country a better place."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["constitution", "constitutional"],
        "response": (
            "The Constitution of Sierra Leone is the supreme law of the country. It was adopted in 1991. "
            "It establishes the structure of government, defines the rights and duties of citizens, and sets out the principles for governing the country. "
            "The Constitution guarantees fundamental rights such as freedom of speech, freedom of assembly, and the right to a fair trial. "
            "Any law that conflicts with the Constitution can be declared invalid by the courts."
        ),
    },

    # ─── History ───

    {
        "subject": "Social Studies",
        "keywords": ["colonial", "colonialism", "colonisation", "british colony", "protectorate"],
        "response": (
            "Sierra Leone was colonized by the British. Freetown was founded in 1787 as a settlement for freed slaves from Britain and North America. "
            "In 1808, the Freetown area became a British Crown Colony. In 1896, the interior became a British Protectorate. "
            "Colonial rule lasted until 1961 when Sierra Leone gained independence. "
            "Colonialism had lasting effects on Sierra Leone's economy, politics, and society."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["slave", "slavery", "slave trade", "abolition", "freed slave"],
        "response": (
            "The transatlantic slave trade involved the forced transport of millions of Africans to the Americas between the 15th and 19th centuries. "
            "Many people from Sierra Leone were captured and sold into slavery. "
            "Britain abolished the slave trade in 1807 and established Freetown as a home for freed slaves. "
            "These freed slaves were called the Krio people, and they developed their own language and culture. "
            "The abolition of the slave trade was a major step toward human rights and justice."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["independence", "1961", "independent"],
        "response": (
            "Sierra Leone became independent from Britain on April 27, 1961. "
            "Sir Milton Margai became the first Prime Minister. Independence Day is celebrated every year on April 27. "
            "After independence, Sierra Leone became a member of the United Nations and the Commonwealth of Nations. "
            "In 1971, Sierra Leone became a republic with Siaka Stevens as the first President."
        ),
    },

    # ─── Geography ───

    {
        "subject": "Social Studies",
        "keywords": ["map", "maps", "compass", "direction", "latitude", "longitude", "equator"],
        "response": (
            "A map is a drawing of a place from above. Maps use symbols and a key to show features like roads, rivers, and towns. "
            "The four main compass directions are north, south, east, and west. "
            "Latitude lines run horizontally around the Earth and measure distance north or south of the Equator. "
            "Longitude lines run from the North Pole to the South Pole and measure distance east or west of the Prime Meridian. "
            "The Equator is an imaginary line around the middle of the Earth that divides it into the Northern and Southern Hemispheres."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["vegetation", "forest", "savannah", "grassland", "mangrove"],
        "response": (
            "Vegetation means the plant life in a region. Sierra Leone has several types of vegetation. "
            "Rainforests are dense forests with tall trees and heavy rainfall, found mainly in the east and south. "
            "Savannah or grassland has scattered trees and grass, found in the north. "
            "Mangrove swamps are found along the coast where saltwater and freshwater mix. "
            "Each type of vegetation supports different plants, animals, and human activities."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["weather", "climate", "rainy season", "dry season", "rainfall", "temperature"],
        "response": (
            "Climate is the average weather pattern over a long period. Sierra Leone has a tropical climate. "
            "There are two main seasons: the rainy season from May to October and the dry season from November to April. "
            "The rainy season brings heavy rainfall, especially along the coast. The dry season is hot and dusty, with harmattan winds from the Sahara Desert. "
            "The average temperature in Sierra Leone is between 24 and 30 degrees Celsius throughout the year."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["population", "census", "population density", "urban", "rural"],
        "response": (
            "Population is the number of people living in a place. A census is an official count of the population. "
            "Population density is the number of people per square kilometre. Densely populated areas have many people, while sparsely populated areas have few. "
            "Urban areas are cities and towns with many people and services. Rural areas are villages and countryside with fewer people. "
            "In Sierra Leone, Freetown is the most densely populated area, while rural areas have lower population density."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["settlement", "village", "town", "city", "urbanisation"],
        "response": (
            "A settlement is a place where people live. Settlements can be small like a village or hamlet, or large like a town or city. "
            "Villages are small rural settlements where people often work in farming. Towns are larger with more services like shops and schools. "
            "Cities are large urban centres with many services, businesses, and job opportunities. "
            "Urbanisation is the movement of people from rural areas to cities, which causes cities to grow."
        ),
    },

    # ─── Economy ───

    {
        "subject": "Social Studies",
        "keywords": ["natural resource", "resources", "diamond", "gold", "bauxite", "rutile", "mineral", "mining"],
        "response": (
            "Natural resources are materials found in nature that people use. "
            "Sierra Leone is rich in minerals, including diamonds, gold, bauxite, rutile, and iron ore. "
            "Diamonds are the most famous mineral resource. Diamond mining provides jobs and income but has also been a source of conflict. "
            "Mining companies extract these resources, which are then exported to other countries. "
            "It is important to manage natural resources wisely so that the benefits are shared fairly and the environment is protected."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["agriculture", "farming", "crop", "rice", "cassava", "cocoa", "coffee", "palm oil", "groundnut", "farmer"],
        "response": (
            "Agriculture is the practice of growing crops and raising animals. It is the main economic activity in Sierra Leone. "
            "Most farmers are small-scale and grow food for their families and to sell at local markets. "
            "Common food crops include rice, cassava, maize, millet, and groundnuts. "
            "Cash crops grown for export include cocoa, coffee, palm oil, and ginger. "
            "Farmers also raise livestock such as cattle, goats, sheep, and chickens."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["fishing", "fish", "coastal", "marine"],
        "response": (
            "Fishing is an important industry in Sierra Leone because of its long coastline and many rivers. "
            "Artisanal fishermen use small boats and traditional methods to catch fish for local communities. "
            "Commercial fishing companies catch larger quantities for export. "
            "Common fish include bonga, tuna, mackerel, and shrimp. "
            "Fishing provides food, jobs, and income for many coastal communities."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["trade", "import", "export", "market", "economy"],
        "response": (
            "Trade is the buying and selling of goods and services. Imports are goods brought into a country from abroad. "
            "Exports are goods sent to other countries. Sierra Leone exports minerals like diamonds and gold, "
            "and agricultural products like cocoa, coffee, and palm oil. "
            "The country imports machinery, fuel, food, and manufactured goods. "
            "A market is where buyers and sellers meet to exchange goods. Local markets are important for everyday trade in Sierra Leone."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["transport", "transportation", "road", "railway", "airport", "sea port"],
        "response": (
            "Transport is how people and goods move from one place to another. "
            "Road transport is the most common in Sierra Leone, with buses, taxis, cars, and motorbikes. "
            "The country has a railway that was historically used for mineral transport. "
            "Freetown has an international airport at Lungi, which is connected to the city by ferry or helicopter. "
            "The main seaport is in Freetown, which handles cargo ships and international trade. "
            "Good transport links are essential for economic development."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["communication", "telephone", "mobile", "internet", "radio", "newspaper"],
        "response": (
            "Communication is how people share information. "
            "In Sierra Leone, radio is the most widely used medium, especially in rural areas. "
            "Mobile phones are very common and used for calls, money transfers, and internet access. "
            "Newspapers and television are available mainly in urban areas. "
            "Communication technology helps people stay connected, learn news, and access services."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["bank", "banking", "savings", "money", "account", "credit"],
        "response": (
            "A bank is a financial institution that keeps money safe for people and provides loans. "
            "Savings accounts allow you to deposit money and earn interest. "
            "Banks also offer loans, which are amounts borrowed that must be paid back with interest. "
            "Mobile money services like Orange Money allow people to send and receive money using their phones. "
            "Saving money regularly helps individuals and families plan for the future."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["tax", "taxation", "revenue", "budget"],
        "response": (
            "Taxes are payments citizens make to the government to fund public services like roads, schools, and hospitals. "
            "The National Revenue Authority, or NRA, collects taxes in Sierra Leone. "
            "Types of taxes include income tax, which is a percentage of what you earn, "
            "and goods and services tax, which is added to the price of many items. "
            "The government creates a budget each year, showing how it plans to collect and spend money."
        ),
    },

    # ─── Culture and Social ───

    {
        "subject": "Social Studies",
        "keywords": ["culture", "tradition", "custom", "ethnic", "tribe"],
        "response": (
            "Culture is the way of life of a group of people, including their language, beliefs, customs, art, and music. "
            "Sierra Leone has rich cultural diversity with many ethnic groups, each with its own traditions. "
            "The Temne are mainly in the north, the Mende in the south and east, and the Krio are mainly in the Western Area. "
            "Other groups include the Limba, Kono, Koranko, Sherbro, and Loko. "
            "Traditional ceremonies, music, dance, and storytelling are important parts of Sierra Leonean culture."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["religion", "religious", "islam", "christianity", "muslim", "christian"],
        "response": (
            "Religion is an important part of life in Sierra Leone. The two main religions are Islam and Christianity. "
            "About three quarters of the population are Muslim, and about one quarter are Christian. "
            "Many people also follow some traditional beliefs and practices. "
            "Sierra Leone is known for religious tolerance, meaning people of different faiths live together peacefully and respect each other."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["family", "extended family", "nuclear family", "marriage", "community"],
        "response": (
            "The family is the basic unit of society. In Sierra Leone, the extended family is very important, including grandparents, aunts, uncles, and cousins. "
            "The nuclear family consists of parents and their children. "
            "Families provide care, support, and education for children. Older family members are respected and cared for. "
            "Communities work together to solve problems and celebrate events. This spirit of togetherness is called communalism."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["education", "school", "primary", "secondary", "university", "literacy"],
        "response": (
            "Education is the process of learning knowledge and skills. In Sierra Leone, education includes primary school for 6 years, junior secondary for 3 years, and senior secondary for 3 years. "
            "The government provides free primary education. After secondary school, students can attend university or other training institutions. "
            "The main universities are Fourah Bay College, Njala University, and the University of Sierra Leone. "
            "Education is important for personal development and for the country's progress."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["health", "hospital", "clinic", "disease", "malaria", "vaccination", "sanitation"],
        "response": (
            "Good health is essential for a productive life. Common health challenges in Sierra Leone include malaria, cholera, and typhoid. "
            "Health facilities include hospitals, clinics, and community health centres. "
            "Vaccinations protect children from diseases like polio and measles. "
            "Clean water and good sanitation are important for preventing disease. "
            "The Ministry of Health works to improve health services and access to care for all citizens."
        ),
    },

    # ─── Africa and World ───

    {
        "subject": "Social Studies",
        "keywords": ["africa", "african", "continent", "african union"],
        "response": (
            "Africa is the second largest continent in the world. It has 54 countries and over 1.4 billion people. "
            "Sierra Leone is located in West Africa. Other West African countries include Liberia, Guinea, Ghana, Nigeria, and Senegal. "
            "The African Union, or AU, is an organization of African countries that works to promote peace, development, and cooperation. "
            "Africa is rich in natural resources and has diverse cultures, languages, and landscapes."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["environment", "pollution", "conservation", "recycling", "deforestation", "climate change"],
        "response": (
            "The environment includes everything around us: the air, water, land, plants, and animals. "
            "Pollution is when harmful substances damage the environment. It can be air pollution from factories, water pollution from waste, or land pollution from litter. "
            "Deforestation is the cutting down of forests, which destroys animal habitats and affects the climate. "
            "Conservation means protecting the environment and using resources wisely. Recycling turns waste into new products. "
            "Climate change is the long-term change in global temperatures and weather patterns, mainly caused by human activities."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["globalisation", "global", "international", "united nations", "un"],
        "response": (
            "Globalization is the increasing connection between countries through trade, technology, and communication. "
            "The United Nations, or UN, is an international organization that works to maintain peace and security, promote human rights, and support development. "
            "Sierra Leone is a member of the United Nations. "
            "Other international organizations include the Commonwealth, the African Union, and the Economic Community of West African States, which is also known as ECOWAS."
        ),
    },
    {
        "subject": "Social Studies",
        "keywords": ["peace", "conflict", "resolution", "mediation", "tolerance"],
        "response": (
            "Peace means living without conflict or violence. Conflict is a disagreement or fight between people or groups. "
            "Conflict resolution is the process of finding a peaceful solution to a disagreement. "
            "Methods include negotiation, where both sides discuss and compromise, and mediation, where a neutral person helps them reach an agreement. "
            "Tolerance means respecting others even when they are different from you. "
            "Building peace requires understanding, dialogue, and a commitment to non-violence."
        ),
    },

# ╔══════════════════════════════════════════════════════════════╗
# ║                   SUBJECT: VOCATIONAL                        ║
# ╚══════════════════════════════════════════════════════════════╝

    # ─── Carpentry ───

    {
        "subject": "Vocational",
        "keywords": ["carpentry", "carpenter", "wood", "woodwork", "furniture", "timber"],
        "response": (
            "Carpentry is the skill of working with wood to make furniture, buildings, and other objects. "
            "A carpenter uses tools like a saw to cut wood, a hammer to drive nails, a plane to smooth surfaces, "
            "a chisel to shape wood, and a measuring tape to measure accurately. "
            "Safety is very important in carpentry. Always wear protective goggles and keep tools sharp and clean. "
            "Carpenters make tables, chairs, doors, window frames, shelves, and roofs. "
            "Carpentry is a valuable trade that provides essential products for homes and businesses."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["wood joint", "joints", "dovetail", "mortise", "tenon"],
        "response": (
            "Wood joints are methods of joining pieces of wood together. Strong joints are important for making furniture that lasts. "
            "A butt joint is the simplest, where two pieces are glued or nailed together end to end. "
            "A mortise and tenon joint is strong and used for tables and chairs. A tenon is a projection that fits into a mortise, which is a hole. "
            "A dovetail joint is very strong and is used for drawers and boxes. The joints interlock like dove tails. "
            "Choosing the right joint depends on the type of furniture and the stress it will承受."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["wood finishing", "varnish", "paint", "stain", "polish", "sanding"],
        "response": (
            "Finishing protects wood and makes it look attractive. Before finishing, sand the wood surface until it is smooth. "
            "Start with rough sandpaper and progress to finer sandpaper. "
            "Varnish gives a clear protective coating that shows the natural wood grain. "
            "Paint adds colour and protection. Stain changes the colour of the wood while still showing the grain. "
            "Apply finish in thin, even coats with a brush or cloth, allowing each coat to dry before applying the next."
        ),
    },

    # ─── Tailoring ───

    {
        "subject": "Vocational",
        "keywords": ["tailoring", "tailor", "sewing", "sew", "fabric", "cloth", "garment", "dressmaking"],
        "response": (
            "Tailoring is the skill of making, repairing, or altering clothing. "
            "A tailor uses tools like a sewing machine, needle, thread, scissors, measuring tape, pins, and an iron. "
            "The first step is taking body measurements, including chest, waist, hips, and length. "
            "Then the fabric is cut according to a pattern. Finally, the pieces are sewn together. "
            "Basic stitches include the running stitch, backstitch, hem stitch, and overcast stitch. "
            "Accurate cutting and careful sewing are essential for a well-fitting garment."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["pattern", "pattern making", "cutting", "fabric cutting"],
        "response": (
            "A pattern is a template used to cut fabric into the right shape for a garment. "
            "Patterns can be bought ready-made or drafted by the tailor. "
            "When cutting fabric, lay the fabric flat and pin the pattern pieces in place. "
            "Cut along the pattern lines carefully with sharp scissors. Follow the grain line, which is the direction of the threads in the fabric. "
            "Always cut on a flat surface and ensure pattern pieces are placed correctly to avoid wasting fabric."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["measurement", "body measurement", "measuring"],
        "response": (
            "Accurate body measurements are essential for well-fitting clothes. "
            "Use a flexible measuring tape. Key measurements include chest or bust, waist, hips, shoulder width, arm length, and full length. "
            "Measure around the body for circumference measurements and from points for length measurements. "
            "The tape should be snug but not tight. Record all measurements clearly. "
            "Different types of garments require different measurements. For example, trousers need waist, hip, and inseam measurements."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["sewing machine", "machine sewing"],
        "response": (
            "A sewing machine stitches fabric quickly and evenly. It uses two threads: one on top and one in a bobbin underneath. "
            "The main parts are the needle, presser foot, feed dogs which move the fabric, and the hand wheel. "
            "Always thread the machine correctly according to the manual. Adjust the stitch length and tension for different fabrics. "
            "Regular maintenance includes cleaning lint from the machine, oiling moving parts, and changing needles when they become blunt."
        ),
    },

    # ─── Cookery ───

    {
        "subject": "Vocational",
        "keywords": ["cooking", "cookery", "food", "recipe", "ingredient", "meal preparation"],
        "response": (
            "Cooking is preparing food by combining ingredients and applying heat. It is an essential life skill. "
            "Basic cooking methods include boiling, frying, roasting, baking, steaming, and grilling. "
            "Hygiene is very important in cooking. Always wash your hands before handling food. Keep raw meat separate from other foods. "
            "Wash fruits and vegetables thoroughly. Store food at the right temperature to prevent spoilage. "
            "A balanced meal includes carbohydrates like rice or cassava, protein like fish or beans, and vegetables."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["baking", "bake", "bread", "cake", "pastry", "oven"],
        "response": (
            "Baking is cooking food using dry heat in an oven. It is used for bread, cakes, pastries, and pies. "
            "The basic ingredients in baking include flour, which provides structure, sugar for sweetness, eggs for binding, "
            "fat or butter for moisture, and baking powder or yeast to make the mixture rise. "
            "Accurate measurement of ingredients is very important in baking. Use measuring cups and spoons. "
            "Preheat the oven to the correct temperature before baking. Test if baked goods are done by inserting a clean toothpick."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["food preservation", "preserving", "drying", "smoking", "salting", "fermentation"],
        "response": (
            "Food preservation stops food from spoiling so it can be stored for longer. "
            "Drying removes water from food, which prevents bacteria from growing. Fish, meat, and fruits can be dried in the sun or using a dryer. "
            "Smoking exposes food to smoke from burning wood, which adds flavour and preserves it. "
            "Salting draws moisture out of food. It is used for fish and meat. "
            "Fermentation uses friendly bacteria to preserve food and create new flavours, like in yoghurt and sour porridge."
        ),
    },

    # ─── Agriculture ───

    {
        "subject": "Vocational",
        "keywords": ["poultry", "chicken", "layer", "broiler", "egg", "chick"],
        "response": (
            "Poultry farming is raising chickens for meat and eggs. Layers are hens raised for egg production. Broilers are chickens raised for meat. "
            "Chickens need a clean coop with proper ventilation, fresh water, and balanced feed. "
            "Layers need nesting boxes where they can lay eggs. Collect eggs daily to keep them clean. "
            "Vaccinate chickens against common diseases like Newcastle disease. Keep the coop clean to prevent illness. "
            "Poultry farming can provide both food and income for a family."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["livestock", "goat", "sheep", "cattle", "animal husbandry"],
        "response": (
            "Livestock farming is raising animals for meat, milk, hides, or as a source of income. "
            "Common livestock in Sierra Leone include goats, sheep, and cattle. Goats are hardy and easy to raise. "
            "Animals need shelter, clean water, adequate food, and veterinary care. Grazing areas should have enough grass. "
            "Regular health checks and vaccinations prevent disease. Proper housing protects animals from rain and predators."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["vegetable", "vegetable farming", "garden", "crop production", "planting", "harvest"],
        "response": (
            "Vegetable farming is growing plants for food. Common vegetables in Sierra Leone include okra, eggplant, tomatoes, peppers, cassava leaves, and bitter leaf. "
            "Prepare the soil by clearing weeds and digging or tilling. Plant seeds or seedlings at the right depth and spacing. "
            "Water plants regularly, especially in the dry season. Remove weeds that compete with crops. "
            "Harvest vegetables when they are ripe. Some vegetables can be harvested multiple times. "
            "Crop rotation, planting different crops each season, helps keep the soil healthy."
        ),
    },

    # ─── Business ───

    {
        "subject": "Vocational",
        "keywords": ["business", "entrepreneur", "entrepreneurship", "enterprise", "start a business"],
        "response": (
            "Entrepreneurship is starting and running your own business. An entrepreneur sees a need in the community and creates a business to meet it. "
            "To start a business, first identify a product or service people need. "
            "Write a simple business plan outlining your product, target customers, pricing, and costs. "
            "You need starting capital, which can come from savings, family, or small loans. "
            "Keep records of your income and expenses. Understand your customers and provide good service. "
            "Starting small and growing gradually is a good approach."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["bookkeeping", "record keeping", "accounts", "income", "expenses", "profit"],
        "response": (
            "Bookkeeping is recording all the money that comes in and goes out of a business. "
            "Income is money from sales. Expenses are money spent on materials, rent, and other costs. "
            "Profit is income minus expenses. If expenses are higher than income, the business makes a loss. "
            "Keep a simple notebook or ledger to record every transaction. Save receipts as proof of purchases. "
            "Good record keeping helps you know if your business is doing well and helps with planning."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["marketing", "sell", "selling", "customer", "price", "advertise"],
        "response": (
            "Marketing is how you let customers know about your products and convince them to buy. "
            "Price your products to cover your costs and make a fair profit, while being affordable for customers. "
            "Good customer service means being friendly, helpful, and reliable. Satisfied customers return and tell others. "
            "Advertising can be through word of mouth, posters, radio, or social media. "
            "Packaging and presentation also matter. Clean, attractive packaging makes products more appealing."
        ),
    },

    # ─── Crafts ───

    {
        "subject": "Vocational",
        "keywords": ["soap making", "soap", "liquid soap", "bar soap"],
        "response": (
            "Soap making is the process of making soap from oils and other ingredients. "
            "For bar soap, the basic ingredients include oil such as palm oil or coconut oil, water, and caustic soda, also called sodium hydroxide. "
            "The oils and caustic soda solution are mixed together in a process called saponification. "
            "You can add colour, fragrance, or herbs to make different types of soap. "
            "Safety is very important because caustic soda is dangerous. Always wear gloves, eye protection, and work in a well-ventilated area."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["tie dye", "tie-dye", "batik", "fabric dyeing"],
        "response": (
            "Tie dye and batik are methods of adding colourful patterns to fabric. "
            "In tie dye, you fold, twist, or tie the fabric with string or rubber bands, then dip it in dye. The tied parts resist the dye and remain white or lighter. "
            "In batik, you use hot wax to draw or stamp patterns on the fabric. The wax resists the dye. "
            "After dyeing, the wax is removed by boiling or ironing to reveal the pattern. "
            "Both methods can create beautiful designs on cotton fabric for clothing and accessories."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["basket weaving", "basket", "mat making", "straw", "raffia", "cane"],
        "response": (
            "Basket weaving and mat making are traditional crafts that use natural materials like straw, raffia, cane, and palm leaves. "
            "The materials are first prepared by soaking them in water to make them flexible. "
            "Then they are woven together using different patterns. "
            "Baskets can be used for storage, carrying goods, or decoration. Mats are used for sleeping, sitting, or drying crops. "
            "These crafts provide income for many rural communities and preserve cultural traditions."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["pottery", "potter", "ceramics", "clay"],
        "response": (
            "Pottery is making objects from clay that are hardened by heat. "
            "First, prepare the clay by kneading it to remove air bubbles. Then shape it using your hands or a potter's wheel. "
            "Common pottery items include pots, bowls, plates, and water jars. "
            "After shaping, the clay must dry completely before firing. "
            "Firing is heating the pottery in a kiln or open fire to make it hard and durable. "
            "Pottery can be decorated with patterns or glazed for a smooth finish."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["leather work", "leather", "tanning", "hide", "bag", "belt", "shoe"],
        "response": (
            "Leather work involves processing animal hides to create useful items. "
            "Tanning is the process of treating animal skin to preserve it and make it soft. "
            "After tanning, the leather can be cut and sewn into products like bags, belts, shoes, wallets, and sandals. "
            "Leather tools include cutting knives, hole punches, needles, and thread. "
            "Good quality leather products can last many years and are valuable for both use and sale."
        ),
    },

    # ─── Building ───

    {
        "subject": "Vocational",
        "keywords": ["building", "construction", "bricklaying", "mason", "cement", "block"],
        "response": (
            "Building construction is the process of creating structures like houses, schools, and shops. "
            "The foundation is the base that supports the building. It must be strong and level. "
            "Walls are built using blocks or bricks held together with cement mortar. "
            "A bricklayer or mason measures, cuts, and lays bricks or blocks in straight lines using a spirit level. "
            "The roof is built with wooden or metal rafters and covered with roofing sheets. "
            "Safety on a construction site includes wearing hard hats, boots, and using tools correctly."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["plumbing", "plumber", "pipe", "water", "tap", "drain"],
        "response": (
            "Plumbing is installing and repairing pipes and fixtures for water supply and drainage. "
            "Plumbers work with pipes made of metal or plastic to bring clean water into buildings and remove waste water. "
            "Common tasks include fixing leaking taps, installing toilets and sinks, and connecting washing machines. "
            "Plumbers use tools like pipe wrenches, hacksaws, and plungers. "
            "Good plumbing is essential for health and hygiene."
        ),
    },
    {
        "subject": "Vocational",
        "keywords": ["welding", "welder", "metal", "iron", "steel", "metalwork"],
        "response": (
            "Welding is joining pieces of metal together by heating them until they melt and fuse. "
            "Common welding methods include arc welding, which uses electricity, and gas welding. "
            "A welder makes gates, window grills, metal doors, tools, and machine parts. "
            "Safety equipment includes a welding helmet with a dark visor to protect the eyes, gloves, and protective clothing. "
            "Welding is a skill that is in high demand in construction and manufacturing."
        ),
    },
]


def find_answer(user_message: str, subject: str = "General") -> str | None:
    message_lower = user_message.lower()
    detected_subject = _classify_subject(user_message)

    for entry in RESPONSES:
        entry_subject = entry["subject"]

        if subject != "General":
            if entry_subject != "General" and entry_subject != subject:
                continue
            if entry_subject == "General":
                if detected_subject and detected_subject != subject:
                    continue

        for keyword in entry["keywords"]:
            if re.search(r"\b" + re.escape(keyword) + r"\b", message_lower):
                return entry["response"]

    return None
