# VeritasAI

## 1. Project Description

Team DTC-02 is developing VeritasAI to help people who read online articles determine the bias and accuracy of the content, and whether it was generated with AI, by implementing AI language models to analyze the text

## 2. Names of Contributors

Team DTC-02:

- Dylan Reimer
- Alex Krantz
- Kyryl Shtanhei
- Daniel Lee
- Travis Gooden

## 3. Technologies and Resources Used

List technologies (with version numbers), API's, icons, fonts, images, media or data sources, and other resources that were used.

### Libraries and frameworks

- ApexCharts (v3.49.1)
- Firebase Admin SDK (v6.5.0)
- Firebase Web SDK (v10.12.1)
- Google Cloud AI Platform SDK (v1.53.0)
- Google Cloud Functions Framework (v3.5.0)
- Google Cloud Logging SDK (v3.10.0)
- Google Cloud Pub/Sub SDK (v2.21.1)
- Google Cloud Storage SDK (v2.16.0)
- IBM Watson (v8.1.0)
- Pydantic (v2.7.1)
- Python Dotenv (v1.0.1)
- Requests (v2.32.2)
- TailwindCSS (v3.4.3)

### Services

- GitHub Actions
- Google Cloud Functions
- Google Cloud Logging
- Google Cloud Pub/Sub
- Google Cloud Storage
- Google Cloud VertexAI
- IBM Watson Natural Language Understanding
- Vercel

### Development Tools

- ESlint (v8.57.0)
- Husky (v9.0.11)
- lint-staged (v15.2.4)
- PDM (v2.15)
- PNPM (v9.1)
- Polylith (v.1.6.0)
- Pytest (v8.2.0)- Prettier (v3.2.5)
- Ruff (v0.4.4)
- SOPS (v3.8.1)

## 4. Complete setup/installion/usage

Here's how to get started once you've cloned the project:

- Install the latest versions of Node.js and Python.
- Install the [pnpm](https://pnpm.io) (Node) and [pdm](https://pdm-project.org/en/stable/) (Python) package managers.
- Install dependencies for each language
  - `pnpm install`
  - `pdm install`
- Install and configure the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
- Configure your `.env` file according to the `.env.example` file.
- Start developing
  - Frontend: `pnpm dev`
  - Backend:
    - Analysis manager: `pdm analysis-manager`
    - Bias analyzer: `pdm bias-analyzer`
    - Tone analyzer: `pdm tone-analyzer`
    - Summary analyzer: `pdm summary-analyzer`
    - Accuracy analyzer: `pdm accuracy-analyzer`

> ![NOTE]
> The full analysis pipeline cannot be fully tested locally due to the use of Google Cloud Pub/Sub.
> However, individual analyzers can be triggered by using the `development/publish.py` script.

Once you've gotten the project running, here's how to use it:

- Login or Signup
- Find an article to scan
- Copy the title, content, author, and publisher into the relevant fields
- Click analyze (wait for ~20 seconds and the pages will populate)

## 5. Known Bugs and Limitations

Here are some known bugs:

- At times, Watson IBM would not generate requested responses
- Using the navigation controls in summary page, it is possible to bypass the lock that waits for another analysis to complete
- Originally, we intended to have guest users. This was not implemented and viewing pages wihtout login breaks the pages
- Bias scans for generic usage of pronouns, adjectives, and sentiment. There is not catagorization into the specific usages of adjectives for positive and negative due to Watson IBM lower-end character limitations. There is not catagorization into specific types of bias, or left/right bias

## 6. Features for Future

What we'd like to build in the future:

- Add AI detection functionality
- Show ranking of different authors and publishers
- Add more advanced bias detection
- Link accuracy detection

## 7. AI usage

- Github Copilot was used to help with line completion during coding
- AI was not used to otherwise generate code or data

- AI App Features:

  - Watson IBM NLU and Google Gemini 1.5 were used for analyzing the submitted articles. Watson IBM responses created the Tone and Bias breakdowns, and Chat GPT 4 created the article summary

- AI Limitations included
  - At times, Watson IBM would not generate requested responses
  - AI detection tools are still in their infancy and still doesn't have a good answer

## 8. Credits

- Hamburger animation to "x" from <https://www.epicweb.dev/tips/hamburger-menu-animation>
- Icons from <https://tablericons.com/>

### Licenses

- Watson NLU: Apache 2.0
- TailwindCSS: MIT
- Firebase: Apache 2.0
- ChatGPT: Proprietary EULA
- ApexCharts: MIT
- Vite: MIT
- Vercel: Proprietary EULA
- PDM: MIT
- PNPM: MIT
- Google Cloud Services: Proprietary EULA
- Google Cloud Python API: Apache 2.0
- Pydantic: MIT
- Eslint: MIT
- Pytest: MIT
- Lint-staged: MIT
- Prettier: MIT
- Husky: MIT
- Ruff: MIT

## 9. Repository Contents

Our backend follows the [Polylith architecture](https://davidvujic.github.io/python-polylith-docs/workspace/), using the `veritasai` namespace. The frontend can be found in the `frontend` folder. The `environments` folder contains
the encrypted configuration for the Google Cloud Functions environment variables.

Content of the project folder:

```shell
# Top level of project folder:
│
├── .env.development  # Environment-suffixed variable files
├── .env.example
├── .env.test
│
├── .eslintignore  # ESLint configuration
├── .eslintrc.json
│
├── .gcloudignore  # Files for Google Cloud and Git to ignore
├── .gitignore
│
├── .lintstagedrc.json
│
├── .prettierignore  # Prettier configuration
├── .prettierrc.json
│
├── .sops.yaml  # SOPS configuration
│
├── firebase.json  # Firebase configuration
├── firestore.indexes.json
├── firestore.rules
│
├── LICENSE.md
├── README.md
│
├── package.json  # NodeJS (PNPM) package specification
├── pnpm-lock.yaml
│
├── pyproject.toml  # Python (PDM) package specification
├── pdm.lock
│
├── tailwind.config.js  # Tailwind CSS configuration
├── postcss.config.js
│
├── vercel.json
├── vite.config.mjs
├── workspace.toml  # Polylith configuration

# It has the following subfolders and files:
│
├── frontend
│   ├── 404.html
│   ├── ai-detect.html
│   ├── analysis.html
│   ├── author.html
│   ├── bias.html
│   ├── dob.html
│   ├── forgot-password.html
│   ├── history.html
│   ├── home.html
│   ├── index.html
│   ├── learn.html
│   ├── login.html
│   ├── profile.html
│   ├── publisher.html
│   ├── saved.html
│   ├── signup.html
│   ├── skeleton.html
│   ├── summary.html
│   ├── tone.html
│   ├── images
│   │   ├── google.svg
│   │   ├── logo.png
│   │   └── logo.svg
│   ├── public  # Static files
│   │   ├── android-chrome-192x192.png
│   │   ├── android-chrome-512x512.png
│   │   ├── apple-touch-icon.png
│   │   ├── browserconfig.xml
│   │   ├── favicon-16x16.png
│   │   ├── favicon-32x32.png
│   │   ├── favicon.ico
│   │   ├── logo.png
│   │   ├── mstile-150x150.png
│   │   ├── safari-pinned-tab.svg
│   │   ├── site.webmanifest
│   │   └── templates  # Shared HTML templates
│   │       ├── analysis-navigation-template.html
│   │       ├── footer-logged-in-template.html
│   │       ├── footer-logged-out-template.html
│   │       └── header-template.html
│   ├── scripts  # Page scripts matching 1:1 with HTML files
│   │   ├── analysis.js
│   │   ├── analysis-navigation.js
│   │   ├── assign-article.js
│   │   ├── authors.js
│   │   ├── bias.js
│   │   ├── firebase.js
│   │   ├── firestore-listener.js
│   │   ├── history.js
│   │   ├── home.js
│   │   ├── learn.js
│   │   ├── nav-bar-logic.js
│   │   ├── profile.js
│   │   ├── publisher.js
│   │   ├── saved.js
│   │   ├── summary.js
│   │   ├── tone.js
│   │   ├── user.js
│   │   ├── authentication  # Authentication-specific scripts
│   │   │   ├── dob.js
│   │   │   ├── forgot-password.js
│   │   │   ├── login.js
│   │   │   ├── logout.js
│   │   │   ├── reset-password.js
│   │   │   ├── shared.js
│   │   │   └── signup.js
│   │   └── firebase_populate  # Scripts/pages for populating Firebase
│   │       ├── firebase_populate_learn_page.html
│   │       └── firebase_populate_learn_page.js
│   └── styles
│       └── tailwind.css
│
├── bases  # The "glue" code connecting the components together
│   ├── .keep
│   └── veritasai
│       ├── accuracy_analyzer  # Analyzes the accuracy of an article
│       │   ├── __init__.py
│       │   └── handler.py
│       ├── analysis_manager  # Manages the analysis process of an article
│       │   ├── __init__.py
│       │   └── handler.py
│       ├── bias_analyzer  # Analyzes the bias of an article
│       │   ├── __init__.py
│       │   └── handler.py
│       ├── summary_analyzer  # Summarizes the content of an article
│       │   ├── __init__.py
│       │   └── handler.py
│       └── tone_analyzer  # Analyzes the tone of an article
│           ├── __init__.py
│           └── handler.py
├── components  # Individual, atomic components of the system
│   ├── .keep
│   └── veritasai
│       ├── accuracy  # Verify accuracy of claims within an article
│       │   ├── __init__.py
│       │   ├── core.py
│       │   └── model.py
│       ├── articles  # Article data model and storage
│       │   ├── __init__.py
│       │   ├── article.py
│       │   ├── dedup.py
│       │   └── storage.py
│       ├── authentication  # Verify Firebase ID tokens
│       │   ├── __init__.py
│       │   └── decorator.py
│       ├── bias  # Detect bias in an article
│       │   ├── __init__.py
│       │   ├── core.py
│       │   ├── scores.py
│       │   └── sentences.py
│       ├── cache  # Check if an article is already in the database
│       │   └── __init__.py
│       ├── config  # Configuration extraction from the environment
│       │   ├── __init__.py
│       │   └── location.py
│       ├── cors  # CORS handling
│       │   ├── __init__.py
│       │   ├── decorator.py
│       │   └── response.py
│       ├── firebase  # Firebase Admin SDK interactions
│       │   ├── __init__.py
│       │   └── app.py
│       ├── input_validation  # HTTP request validation
│       │   ├── __init__.py
│       │   ├── error.py
│       │   └── models.py
│       ├── logging  # Environment-based logging
│       │   └── __init__.py
│       ├── pubsub  # Google Cloud Pub/Sub interactions
│       │   ├── __init__.py
│       │   ├── publisher.py
│       │   └── topics.py
│       ├── summarizer  # Summarize the content of an article
│       │   ├── __init__.py
│       │   ├── core.py
│       │   └── model.py
│       ├── tone  # Detect the tone of an article
│       │   ├── __init__.py
│       │   ├── core.py
│       │   ├── plutchik.py
│       │   └── summary.py
│       └── watson  # IBM Watson Natural Language Understanding interactions
│           ├── __init__.py
│           └── language.py
├── development  # Development scripts for testing and experimentation
│   ├── .keep
│   ├── __init__.py
│   ├── function.py
│   ├── populate.py
│   ├── publish.py
│   └── testsupport
│       ├── __init__.py
│       └── config.py
├── projects  # The deployable instances of the bases
│   ├── .keep
│   ├── accuracy-analyzer
│   │   ├── main.py
│   │   └── pyproject.toml
│   ├── analysis-manager
│   │   ├── main.py
│   │   └── pyproject.toml
│   ├── bias-analyzer
│   │   ├── main.py
│   │   └── pyproject.toml
│   ├── summary-analyzer
│   │   ├── main.py
│   │   └── pyproject.toml
│   └── tone-analyzer
│       ├── main.py
│       └── pyproject.toml
├── test  # Unit tests
│   ├── conftest.py
│   ├── bases
│   │   └── veritasai
│   │       ├── accuracy_analyzer
│   │       │   └── __init__.py
│   │       ├── analysis_manager
│   │       │   ├── __init__.py
│   │       │   └── test_validation.py
│   │       ├── bias_analyzer
│   │       │   └── __init__.py
│   │       ├── summary_analyzer
│   │       │   └── __init__.py
│   │       └── tone_analyzer
│   │           └── __init__.py
│   └── components
│       └── veritasai
│           ├── accuracy
│           │   └── __init__.py
│           ├── articles
│           │   ├── __init__.py
│           │   ├── test_article_content.py
│           │   ├── test_article_from_cloud_event.py
│           │   ├── test_article_from_input.py
│           │   ├── test_article.py
│           │   ├── test_article_to_dict.py
│           │   ├── test_generate_id.py
│           │   └── test_storage.py
│           ├── authentication
│           │   ├── __init__.py
│           │   └── test_decorator.py
│           ├── bias
│           │   └── __init__.py
│           ├── cache
│           │   ├── __init__.py
│           │   └── test_has_article.py
│           ├── config
│           │   ├── __init__.py
│           │   └── location.py
│           ├── cors
│           │   ├── __init__.py
│           │   ├── test_add_cors_headers.py
│           │   ├── test_allowed_origin.py
│           │   └── test_decorator.py
│           ├── firebase
│           │   ├── __init__.py
│           │   ├── test_credentials.py
│           │   └── testdata
│           │       └── service_account.json
│           ├── input_validation
│           │   ├── __init__.py
│           │   └── test_analyze_text.py
│           ├── pubsub
│           │   ├── __init__.py
│           │   ├── test_publisher.py
│           │   └── test_topics.py
│           ├── summarizer
│           │   ├── conftest.py
│           │   ├── __init__.py
│           │   ├── test_model.py
│           │   └── test_summarize.py
│           ├── tone
│           │   └── __init__.py
│           └── watson
│               ├── __init__.py
│               └── test_language.py
├── environments  # Encrypted environment variables for Google Cloud Functions
│   ├── accuracy-analyzer.yaml
│   ├── analysis-manager.yaml
│   ├── bias-analyzer.yaml
│   ├── summary-analyzer.yaml
│   └── tone-analyzer.yaml
├── .github
│   └── workflows  # GitHub Actions workflows
│       ├── build.yml  # Build each base
│       ├── deploy.yml  # Automatically deploy everything
│       ├── lint.yml  # Code quality checks
│       └── test.yml  # Run unit tests
├── .husky  # Git pre-commit hooks
│   └── pre-commit
└── .vscode  # Workspace VSCode settings
    ├── extensions.json
    ├── launch.json
    └── settings.json
```

## 10. Contact Info

| Name           | Email                     | Github                             |
| -------------- | ------------------------- | ---------------------------------- |
| Alex Krantz    | <alex@krantz.dev>         | <https://github.com/akrantz01>     |
| Daniel Lee     | <dancheuklee@gmail.com>   | <https://github.com/dlee537>       |
| Dylan Reimer   | <reimer.dylan@gmail.com>  | <https://github.com/twistedburger> |
| Kyryl Shtanhei | <kyryl@shtanhei.org>      | <https://github.com/kyrylshtanhei> |
| Travis Gooden  | <travis.gooden@gmail.com> | <https://github.com/travis-aaron>  |
