# ESG Greenwashing Analysis Frontend

This is a frontend application based on React + TypeScript + Vite for ESG (Environmental, Social, and Governance) greenwashing analysis. The project provides document upload, chat interaction, ESG report analysis, and data visualization features.

## Features

* Document upload and preview (PDF, HTML, etc.)
* AI chat system
* ESG report analysis and greenwashing detection
* Multilingual support (English, Italian, German)
* Responsive design and modern UI
* Data visualization and dashboards

## Prerequisites

* Node.js 18+
* npm, yarn, or bun
* Modern browser (Chrome, Firefox, Safari, Edge)

## Installation and Setup

### Using npm (recommended)

1. **Install dependencies**:

```bash
cd frontend/v2

# Install dependencies
npm install
```

2. **Start the development server**:

```bash
# Start development server (with hot reload)
npm run dev
```

## Running the App

### Development Mode

```bash
# Start development server (with hot reload)
npm run dev
```

The app will run at [http://localhost:8080](http://localhost:8080)

### Build Production Version

```bash
# Build production version
npm run build

# Preview production build
npm run preview
```

### Development Build

```bash
# Build development version
npm run build:dev
```

## Project Directory Structure

```
frontend/v2/
├── public/                    # Static assets
│   ├── favicon.ico           # Website icon
│   ├── placeholder.svg       # Placeholder image
│   └── robots.txt            # Search engine crawler configuration
├── src/                      # Source code directory
│   ├── components/           # Reusable components
│   │   ├── ui/              # UI base components (shadcn/ui)
│   │   ├── EnhancedCompanyReport.tsx  # Company report enhancement component
│   │   ├── FloatingChatbot.tsx        # Floating chatbot
│   │   ├── LanguageSelector.tsx       # Language selector
│   │   ├── Seo.tsx                    # SEO component
│   │   └── TopNav.tsx                 # Top navigation
│   ├── config/              # Configuration management
│   │   └── api.config.ts    # API configuration
│   ├── features/            # Feature modules
│   │   └── chat/            # Chat functionality
│   │       ├── components/  # Chat components
│   │       └── hooks/       # Chat hooks
│   ├── hooks/               # Custom hooks
│   │   ├── use-mobile.tsx   # Mobile detection hook
│   │   ├── use-toast.ts     # Toast notification hook
│   │   └── useLanguage.ts   # Language hook
│   ├── i18n/                # Internationalization configuration
│   │   ├── index.ts         # i18n initialization
│   │   └── locales/         # Language files
│   │       ├── de.json      # German translation
│   │       ├── en.json      # English translation
│   │       └── it.json      # Italian translation
│   ├── lib/                 # Utility library
│   │   └── utils.ts         # Utility functions
│   ├── pages/               # Page components
│   │   ├── Chat.tsx         # Chat page
│   │   ├── Company.tsx      # Company analysis page
│   │   ├── Index.tsx        # Homepage
│   │   ├── NotFound.tsx     # 404 page
│   │   └── Upload.tsx       # File upload page
│   ├── services/            # API services
│   │   └── api.service.ts   # API service wrapper
│   ├── App.css              # App styles
│   ├── App.tsx              # Root component
│   ├── index.css            # Global styles
│   ├── main.tsx             # App entry point
│   └── vite-env.d.ts        # Vite environment types
├── .gitignore               # Git ignore configuration
├── bun.lockb                # Bun lock file
├── components.json          # shadcn/ui component configuration
├── eslint.config.js         # ESLint configuration
├── index.html               # HTML template
├── package.json             # Project configuration and dependencies
├── package-lock.json        # npm lock file
├── postcss.config.js        # PostCSS configuration
├── tailwind.config.ts       # Tailwind CSS configuration
├── tsconfig.app.json        # TypeScript app configuration
├── tsconfig.json            # TypeScript configuration
├── tsconfig.node.json       # TypeScript Node configuration
├── vite.config.ts           # Vite configuration
└── README.md                # Project documentation
```

## Tech Stack

* **Framework**: React 18 + TypeScript
* **Build Tool**: Vite
* **Styling**: Tailwind CSS + shadcn/ui
* **Routing**: React Router v6
* **State Management**: React Query + React Hook Form
* **Internationalization**: i18next
* **UI Components**: Radix UI + Lucide React
* **Charts**: Recharts
* **HTTP Client**: Axios
* **Form Validation**: Zod

## Development Guide

### Adding New Dependencies

Install packages using npm:

```bash
npm install package-name
```

### Code Standards and Quality

The project uses ESLint for code linting:

```bash
# Run code linting
npm run lint
```

### Adding a New Language

1. Create a new language file (e.g., `fr.json`) in `src/i18n/locales/`
2. Add the new language configuration in `src/i18n/index.ts`
3. Update the language selector component to support the new language

### Custom Theme

The project uses Tailwind CSS. You can customize the theme by modifying `tailwind.config.ts`:

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#007bff',
          dark: '#0056b3',
        },
      },
    },
  },
}
```

## API Integration

The frontend integrates with backend APIs. Main API endpoints include:

* Document upload: `POST /api/upload`
* Chat interaction: `POST /api/chat`
* ESG report analysis: `GET /api/report/{id}`
* Dashboard data: `GET /api/dashboard`

API configuration is located in `src/config/api.config.ts` and can be adjusted according to backend deployment.
