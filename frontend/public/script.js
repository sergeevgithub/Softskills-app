const tasks = {
    "test_1": [
        {
            "question": "Two software developers disagree on whether to use a JavaScript framework or a native approach for building a web application.",
            "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict", "Structural Conflict", "Value-Based Conflict"],
            "right_choices": 0
        }
    ],
    "test_2": [
        {
            "question": "An engineer faces a dilemma between taking a lucrative job offer in a high-tech industry or continuing to work on a startup with a passion for renewable energy.",
            "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict", "Structural Conflict", "Value-Based Conflict"],
            "right_choices": 1
        }
    ],
    "test_3": [
        {
            "question": "A university's engineering department is reorganized, leading to confusion about new roles and responsibilities within the team.",
            "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict", "Structural Conflict", "Value-Based Conflict"],
            "right_choices": 3
        }
    ],
    "test_4": [
        {
            "question": "A team of researchers with different cultural backgrounds struggles to agree on how to design their experiment.",
            "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict", "Structural Conflict", "Value-Based Conflict"],
            "right_choices": 4
        }
    ],
    "test_5": [
        {
            "question": "A project manager needs to decide whether to prioritize a technical feature or focus on user experience for an upcoming product launch.",
            "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict", "Structural Conflict", "Value-Based Conflict"],
            "right_choices": 1
        }
    ],
    "test_6": [
        {
            "question": "Two team members in a robotics club argue over the allocation of project resources, each believing their approach is more efficient.",
            "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict", "Structural Conflict", "Value-Based Conflict"],
            "right_choices": 0
        }
    ],
    "test_7": [
        {
            "question": "A large tech company faces disagreements among top-level executives about the company's future direction, especially regarding artificial intelligence versus traditional computing.",
            "choices": ["Interpersonal Conflict", "Intrapersonal Conflict", "Organizational Conflict", "Structural Conflict", "Value-Based Conflict"],
            "right_choices": 2
        }
    ]
};

let currentTestIndex = 0;
let currentQuestionIndex = 0;

function loadQuestion() {
    const nextButton = document.getElementById('next-question');
    nextButton.disabled = true;

    const testName = `test_${currentTestIndex + 1}`;
    const currentTest = tasks[testName];
    const currentQuestion = currentTest[currentQuestionIndex];

    const questionContainer = document.getElementById('question-container');
    questionContainer.innerHTML = '';

    const questionElement = document.createElement('div');
    questionElement.innerHTML = `<p><strong>Question ${currentTestIndex + 1}:</strong> ${currentQuestion.question}</p>`;

    const choicesList = document.createElement('ul');
    choicesList.classList.add('choices');

    currentQuestion.choices.forEach((choice, index) => {
        const choiceItem = document.createElement('li');
        choiceItem.classList.add('choice');
        choiceItem.innerText = choice;
        choiceItem.onclick = () => selectChoice(index);
        choicesList.appendChild(choiceItem);
    });

    questionContainer.appendChild(questionElement);
    questionContainer.appendChild(choicesList);
}

function selectChoice(choiceIndex) {
    const testName = `test_${currentTestIndex + 1}`;
    const currentTest = tasks[testName];
    const currentQuestion = currentTest[currentQuestionIndex];

    const choices = document.querySelectorAll('.choice');
    choices.forEach((choice, index) => {
        choice.classList.remove('selected');
        choice.classList.remove('correct');
        choice.classList.remove('incorrect');
        if (index === choiceIndex) {
            choice.classList.add('selected');
        }
    });

    const result = document.getElementById('result');
    const nextButton = document.getElementById('next-question');

    // Disable next question button initially, and will only enable if the correct choice is selected
    nextButton.disabled = true;
    nextButton.classList.remove('enabled');

    if (choiceIndex === currentQuestion.right_choices) {
        result.textContent = "Correct! You've matched the scenario with the right conflict type.";
        choices[choiceIndex].classList.add('correct');
        nextButton.disabled = false;
        nextButton.classList.add('enabled');
    } else {
        result.textContent = "Incorrect. Please review the correct classification.";
        choices[choiceIndex].classList.add('incorrect');
    }
}

function nextQuestion() {
    const testName = `test_${currentTestIndex + 1}`;
    const currentTest = tasks[testName];
    const currentQuestion = currentTest[currentQuestionIndex];

    const choices = document.querySelectorAll('.choice');
    choices.forEach(choice => {
        choice.classList.remove('selected');
        choice.classList.remove('correct');
        choice.classList.remove('incorrect');
    });

    currentQuestionIndex++;

    if (currentQuestionIndex < currentTest.length) {
        loadQuestion();
    } else {
        currentTestIndex++;
        currentQuestionIndex = 0;

        if (currentTestIndex < Object.keys(tasks).length) {
            loadQuestion();
        } else {
            alert('Congratulations, you have completed the task!');
        }
    }
}

loadQuestion();
