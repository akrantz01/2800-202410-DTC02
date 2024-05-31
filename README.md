# VeritasAI

## 1. Project Description

Team DTC02 is developing VeritasAI to help people who read online articles determine the bias and accuracy of the content, and whether it was generated with AI, by implementing AI language models to analyze the text

## 2. Names of Contributors

- DTC-02
- Dylan Reimer
- Alex Krantz
- Kyryl Shtanhei
- Daniel Lee
- Travis Gooden

## 3. Technologies and Resources Used

List technologies (with version numbers), API's, icons, fonts, images, media or data sources, and other resources that were used.

- HTML, CSS, JavaScript
- Tailwind v3.4.3
- Firebase v10.12.1
- Firebase admin v6.5.0
- ChatGPT v3.5
- IBM Watson v8.1.0
- ApexCharts v3.49.1
- Vite v5.2.11
- Vercel v???
- PDM v2.15.2
- PNPM v9.1.0
- Google Cloud v 0.34.0
- Google Cloud Storage v2.16.0
- Google Cloud pubsub v2.21.1
- Google Cloud firestore v2.16.0
- Google api python client
- Pydantic v2.7.1
- Pytest v8.2.0
- Eslint v8.57.0
- Lint-staged v15.2.4
- Prettier v3.2.5
- Husky v9.0.11
- Ruff v0.4.4

## 4. Complete setup/installion/usage

Here's how to get started once you've cloned the project:

- Install the [pnpm](https://pnpm.io) (Node) and [pdm](https://pdm-project.org/en/stable/) (Python) package managers.
- Install dependencies for each language
  - `pnpm install`
  - `pdm install`
- Start developing
  - Frontend: `pnpm dev`
  - Backend: TBD

## 5. Known Bugs and Limitations

Here are some known bugs:

- ...
- ...
- ...

## 6. Features for Future

What we'd like to build in the future:

- Add AI detection functionality
- Show ranking of different authors and publishers
- Add more advanced bias detection
- Link accuracy detection

## 7. Contents of Folder

Content of the project folder:

```text
 Top level of project folder:
├── .env
├── .env.development
├── .env.example
├── .env.test
├── .eslintignore
├── .eslintrc.json
├── .gcloudignore
├── .gitignore
├── .lintstagedrc.json
├── .pdm-python
├── .prettierignore
├── .prettierrc.json
├── .sops.yaml
├── firebase.json
├── firestore.indexes.json
├── firestore.rules
├── LICENSE.md
├── package-lock.json
├── package.json
├── pdm.lock
├── pnpm-lock.yaml
├── postcss.config.js
├── pyproject.toml
├── README.md
├── tailwind.config.js
├── vercel.json
├── vite.config.mjs
└── workspace.toml


It has the following subfolders and files:
├── .github\workflows
│       ├── deploy.yml
│       ├── lint.yml
│       └── test.yml
├── .husky
│       ├── _
│       └── pre-commit
├── .idea
├── .pytest_cache
├── .ruff_cache
├── .venv
├── .vscode
├── bases
│       ├── veritasai
│       │       ├── analysis_manager
│       │       │   ├── __init__.py
│       │       │   └── handler.py
│       │       ├── bias_analyzer
│       │       │   ├── __init__.py
│       │       │   └── handler.py
│       │       └── tone_analyzer
│       │           ├── __init__.py
│       │           └── handler.py
│       └── .keep
├── components
│       ├── veritasai
│       │       ├── articles
│       │       │   ├── __init__.py
│       │       │   ├── article.py
│       │       │   ├── dedup.py
│       │       │   └── storage.py
│       │       ├── authentication
│       │       │   ├── __init__.py
│       │       │   └── decorator.py
│       │       ├── bias
│       │       │   ├── __init__.py
│       │       │   ├── core.py
│       │       │   ├── scores.py
│       │       │   └── sentences.py
│       │       ├── cache
│       │       │   └── __init__.py
│       │       ├── config
│       │       │   ├── __init__.py
│       │       │   └── location.py
│       │       ├── cors
│       │       │   ├── __init__.py
│       │       │   ├── decorator.py
│       │       │   └── resonse.py
│       │       ├── firebase
│       │       │   ├── __init__.py
│       │       │   └── app.py
│       │       ├── input_validation
│       │       │   ├── __init__.py
│       │       │   ├── error.py
│       │       │   └── models.py
│       │       ├── logging
│       │       │   └── __init__.py
│       │       ├── pubsub
│       │       │   ├── __init__.py
│       │       │   ├── publisher.py
│       │       │   └── topics.py
│       │       ├── tone
│       │       │   ├── __init__.py
│       │       │   ├── core.py
│       │       │   ├── plutchik.py
│       │       │   └── summary.py
│       │       └── watson
│       │           ├── __init__.py
│       │           └── language.py
│       └── .keep
├── development
│       ├── testsupport
│       │       ├── __init__.py
│       │       └── config.py
│       ├── __init__.py
│       ├── .keep
│       ├── function.py
│       ├── popukate.py
│       └── publish.py
├── environments
│       ├── analysis-manager.yaml
│       ├── bias-analyzer.yaml
│       └── tone-analyzer.yaml
├── frontend
│       ├── images
│       │       ├── google.svg
│       │       ├── logo.png
│       │       └── logo.svg
│       ├── public
│       │       ├── fonts
│       │       │   └── OpenSans-Regular.ttf
│       │       ├── templates
│       │       │   ├── analysis-navigation-template.html
│       │       │   ├── footer-logged-in-template.html
│       │       │   ├── footer-logged-out-template.html
│       │       │   └── header-template.html
│       │       ├── android-chrome-192x192.png
│       │       ├── android-chrome-512x512.png
│       │       ├── apple-touch-icon.pnh
│       │       ├── browserconfig.xml
│       │       ├── favicon-16x16.png
│       │       ├── favicon-32x32.png
│       │       ├── favicon.ico
│       │       ├── logo.png
│       │       ├── mstile-150x150.png
│       │       ├── safari-pinned-tab.svg
│       │       └── site.webmanifest
│       ├── scripts
│       │       ├── authentication
│       │       │   ├── dob.js
│       │       │   ├── forgot-password.js
│       │       │   ├── login.js
│       │       │   ├── logout.js
│       │       │   ├── reset-password.js
│       │       │   ├── shared.js
│       │       │   └── signup.js
│       │       ├── firebase_populate
│       │       │   ├── firebase_populate_learn_page.html
│       │       │   └── firebase_populate_learn_page.js
│       │       ├── analysis-navigation.js
│       │       ├── analysis.js
│       │       ├── assign-article.js
│       │       ├── authors.js
│       │       ├── bias.js
│       │       ├── firestore.js
│       │       ├── firestore-listener.js
│       │       ├── history.js
│       │       ├── home.js
│       │       ├── learn.js
│       │       ├── nav-bar-logic.js
│       │       ├── profile.js
│       │       ├── publisher.js
│       │       ├── saved.js
│       │       ├── summary.js
│       │       ├── tone.js
│       │       └── user.js
│       ├── styles
│       │       ├── output.css
│       │       └── tailwind.css
│       ├── 404.html
│       ├── ai-detect.html
│       ├── analysis.html
│       ├── author.html
│       ├── bias.html
│       ├── dob.html
│       ├── forgot-password.html
│       ├── history.html
│       ├── home.html
│       ├── index.html
│       ├── learn.html
│       ├── login.html
│       ├── profile.html
│       ├── publisher.html
│       ├── saved.html
│       ├── signup.html
│       ├── skeleton.html
│       ├── summary.html
│       └── tone.html
├── node_modules
├── projects
│       ├── analysis-manager
│       │       ├── main.py
│       │       └── pyproject.toml
│       ├── bias-analyzer
│       │       ├── main.py
│       │       └── pyproject.toml
│       ├── tone-analyzer
│       │       ├── main.py
│       │       └── pyproject.toml
│       ├── .keep
├── test
│       ├── bases
│       │   └── veritasai
│       │       ├── analysis_manager
│       │       │   ├── __init__.py
│       │       │   └── test_validation.py
│       │       ├── bias_analyzer
│       │       │   └── __init__.py
│       │       └── tone_analyzer
│       │           └── __init__.py
│       └── components
│           └── veritasai
│               ├── articles
│               │   ├── __init__.py
│               │   ├── test_article_content.py
│               │   ├── test_article_from_cloud_event.py
│               │   ├── test_article_from_input.py
│               │   ├── test_article_to_dict.py
│               │   ├── test_article.py
│               │   ├── test_generate_id.py
│               │   └── test_storage.py
│               ├── authentication
│               │   ├── __init__.py
│               │   └── test_decorator.py
│               ├── bias
│               │   └── __init__.py
│               ├── cache
│               │   ├── __init__.py
│               │   └── test_has_article.py
│               ├── config
│               │   ├── __init__.py
│               │   └── location.py
│               ├── cors
│               │   ├── __init__.py
│               │   ├── test_add_cors_headers.py
│               │   ├── test_allowed_origin.py
│               │   └── test_decorator.py
│               ├── document_id
│               ├── firebase
│               │   ├── testdata
│               │   │   └── service_account.json
│               │   ├── __init__.py
│               │   ├── test_credentials.py
│               │   ├── input_validation
│               │   │   ├── __init__.py
│               │   │   └── test_analyze_text.py
│               │   ├── pubsub
│               │   │   ├── __init__.py
│               │   │   ├── test_publisher.py
│               │   │   └── test_topics.py
│               │   ├── tone
│               │   │   └── __init__.py
│               │   └── watson
│               │       ├── __init__.py
│               │       └── test_language.py
│               └── conftest.py
```
