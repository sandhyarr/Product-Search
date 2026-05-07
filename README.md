# AdNabu Product Search Automation

AdNabu Product Search Automation is a Selenium-based automation testing project developed using Python for testing core e-commerce functionalities such as product search and add-to-cart workflow.

This project was created as part of a QA Automation assessment for the web application **AdNabuTestStore**, an online e-commerce platform.

---

# Project Objective

The objective of this project is to:

* Design high-quality test cases for Product Search and Add to Cart modules
* Automate the product search and add-to-cart functionality
* Validate the successful user workflow in an e-commerce application
* Demonstrate Selenium automation using Python with proper waits and modular code structure

---

# Working Model

The automation process follows a real-time user shopping workflow:

1. Open the browser
2. Launch the AdNabuTestStore website
3. Search for a product using the search bar
4. Display matching search results
5. Select the required product
6. Open the product details page
7. Add the product to the cart
8. Verify the product is successfully added to the cart
9. Complete the automation execution

---

# Features Covered

## Product Search

* Search products using keywords
* Validate search results
* Handle invalid searches
* Verify product visibility

## Add to Cart

* Add product to shopping cart
* Verify successful cart addition
* Validate cart workflow
* Basic end-to-end shopping validation

---

# Technologies Used

* Python
* Selenium WebDriver
* ChromeDriver
* Explicit Waits

---

# Project Structure

```text
Adnabu Automation script/
│
├── README.md
├── requirements.txt
├── reports/
│   └── latest_run.txt
│
└── tests/
    └── product_search.py
```

---

# Automation Requirements Followed

* Used Python with Selenium
* Implemented proper waits instead of hardcoded sleeps
* Maintained readable and modular code
* Performed end-to-end product search and cart validation

---

# Scope of Project

This project focuses only on the requested automation scenario and does not include:

* Full automation framework setup
* Cross-browser execution
* Advanced reporting tools
* Complete application test coverage

---

# Expected Outcome

The automation script should successfully:

* Open the e-commerce website
* Search for the required product
* Add the product to the shopping cart
* Validate successful cart addition without failures

---

# Purpose of the Project

This project demonstrates practical QA Automation skills including:

* Manual test design
* Selenium automation
* E-commerce workflow validation
* Basic automation scripting using Python
* Real-time user scenario testing
