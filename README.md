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
- Firestore v2.16.0
- ChatGPT v3.5
- IBM Watson v8.1.0
- ApexCharts v3.49.1
- Vite v5.2.11
- Vercel v???
- PDM
- PNPM
- Google Cloud Storage/Services - multiple versions
- Pub/sub
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
... my chatgpt wont take screenshots at the moment so I cant add the rest
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
│       ├── components
│       │   └── veritasai
│       │       ├── articles
│       │       │   ├── __init__.py
│       │       │   ├── test_article_content.py
│       │       │   ├── test_article_from_cloud_event.py
│       │       │   ├── test_article_from_input.py
│       │       │   ├── test_article_to_dict.py
│       │       │   ├── test_article.py
│       │       │   ├── test_generate_id.py
│       │       │   └── test_storage.py
│       │       ├── authentication
│       │       │   ├── __init__.py
│       │       │   └── test_decorator.py
│       │       ├── bias
│       │       │   └── __init__.py
│       │       ├── cache
│       │       │   ├── __init__.py
│       │       │   └── test_has_article.py
│       │       ├── config
│       │       │   ├── __init__.py
│       │       │   └── location.py
│       │       ├── cors
│       │       │   ├── __init__.py
│       │       │   ├── test_add_cors_headers.py
│       │       │   ├── test_allowed_origin.py
│       │       │   └── test_decorator.py
│       │       ├── document_id
│       │       ├── firebase
│       │       │   ├── testdata
│       │       │   │   └── service_account.json
│       │       │   ├── __init__.py
│       │       │   ├── test_credentials.py
│       │       │   ├── input_validation
│       │       │   │   ├── __init__.py
│       │       │   │   └── test_analyze_text.py
│       │       │   ├── pubsub
│       │       │   │   ├── __init__.py
│       │       │   │   ├── test_publisher.py
│       │       │   │   └── test_topics.py
│       │       │   ├── tone
│       │       │   │   └── __init__.py
│       │       │   └── watson
│       │       │       ├── __init__.py
│       │       │       └── test_language.py
│       │       └── conftest.py
```
