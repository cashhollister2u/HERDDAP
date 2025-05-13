// This is a Next.js page component that serves as the landing page for the application.
export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <h1> TO DO: Landing Page</h1>
        <h2>Active Pages:</h2>
        <a href="/griddap">/griddap</a>
      </main>
    </div>
  );
}