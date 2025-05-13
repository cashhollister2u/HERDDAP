### Notes:

- Using fastAPI to cache data ahead of time is slightly faster.
- Look into using fastAPI for loading static files instead of NextJS.
    - Use Jinja2 to pass python variables to html similarly to how NextJS does.
    - Remove caching functionality if not needed.
    
## Backend

Run the fastAPI server:

```bash
cd backend
```

```bash
uvicorn main:app --reload
```

## Frontend

Run the development server:

```bash
cd frontend_js
```

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```


