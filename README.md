# Django Website Analysis Tool

## Description
This tool, built with Django, is engineered for analyzing websites. It generates in-depth reports focusing on UX/UI design, trust signals, and other technical aspects. The project is divided into three primary components: Website Analyzer, API, and Report Generation.

### Features
- **UX/UI Analysis**: Assesses elements like call-to-action buttons, form design, and message clarity.
- **Trust Signals**: Identifies social proofs such as testimonials, certifications, partner logos, and company details.
- **Report Generation**: Compiles detailed reports from the analysis, pinpointing areas for improvement and strengths.

## Installation
To set up this project, follow these steps:

```
git clone https://github.com/IndiasFernandes/websiteAudit
cd websiteAudit
pip install -r requirements.txt
```


## Usage
Run the Django server and interact with the tool as follows:
```
python manage.py runserver
```

- Make a POST request to `/api/analyze` with the website URL for analysis.
- Access the generated report from `/reports/{report_id}`.

## Contributing
Contributions are welcome! If you have improvements or bug fixes:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License
This project is licensed under the "GNU General Public License v3.0".

## Acknowledgements
- A shoutout to all contributors and maintainers.
- Special thanks to [Special Mentions].
