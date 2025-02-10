# FacePay - Face Recognition Payment System

**Slogan**: _Face the Future, Pay Without the QR!_

FacePay is an innovative, secure, and convenient payment system that leverages facial recognition technology to make payments without the need for QR codes. By using cutting-edge facial recognition, users can easily authenticate and complete transactions just by showing their face. This project integrates modern web development techniques with state-of-the-art AI-powered face recognition, creating a seamless payment experience.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Introduction

FacePay is designed to provide a quick and secure way to make payments and request money using facial recognition. It eliminates the need for traditional methods like QR codes or UPI PINs. Users can simply log in to the system by scanning their face, and the payment or request is verified using their facial features. This app offers a modern user interface and integrates with the latest technologies for seamless user experience.

### Key Features:
- **Face Recognition Login**: Log in securely using your face.
- **Face-Based Payments**: Make payments simply by scanning your face.
- **Request Money**: Easily send payment requests to other users using their face recognition.
- **No QR Code Required**: Say goodbye to QR codes for payments, face authentication is enough!
- **Seamless UI**: User-friendly design for easy interaction and quick payments.

## Features

- **Live Face Detection**: Uses live video feed for real-time face recognition.
- **Payment Gateway Integration**: Though not implemented here, the system can be easily extended to integrate with a payment gateway for actual transactions.
- **User Registration**: Easy sign-up process with face capture and secure login.
- **Secure and Private**: Facial data is stored securely, and all communications are encrypted.
- **Attractive UI**: Sleek, modern interface for a pleasant user experience.
- **Cross-platform**: Works seamlessly on desktops, tablets, and smartphones.

## Technology Stack

- **Flask**: Web framework for building the backend.
- **DeepFace**: Python library for facial recognition.
- **OpenCV**: Used for capturing video feeds from the webcam.
- **SQLite**: Lightweight database to store user information.
- **HTML, CSS, JavaScript**: For front-end UI design and interactivity.
- **Bootstrap**: For responsive, mobile-first web design.
- **jQuery**: For handling frontend operations and AJAX requests.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/facepay.git
    cd facepay
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```bash
    python app.py
    ```

5. Visit `http://127.0.0.1:5000` in your browser to start using the FacePay application.

## Usage

### 1. **User Registration**
   - To use FacePay, start by registering with your face.
   - Once registered, you can login with your facial features.
   
### 2. **Login**
   - After registration, log in using the live face scan.
   - Once authenticated, you can make payments, request money, or view your balance.

### 3. **Payment**
   - After logging in, select the "Pay" option, enter the amount, and confirm the transaction with face recognition.

### 4. **Ask for Payment**
   - Users can request money from others with their face as the unique ID.

<!-- ## Screenshots

Here are some screenshots of the application:

### Login Page:

![Login Page](https://via.placeholder.com/600x400.png?text=Login+Page)

### Register Page:

![Register Page](https://via.placeholder.com/600x400.png?text=Register+Page)

### Payment Screen:

![Payment Screen](https://via.placeholder.com/600x400.png?text=Payment+Screen)

### Live Face Scan:

![Live Face Scan](https://via.placeholder.com/600x400.png?text=Live+Face+Scan) -->

## Contributing

We welcome contributions to this project! Feel free to fork the repository, create a branch, and submit a pull request. If you're reporting a bug or suggesting an enhancement, please open an issue.

### Steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new Pull Request.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

**Face the Future, Pay Without the QR!**