import { Bot, ChefHat, ListChecks } from 'lucide-react'

function App() {
  return (
    <main className="min-h-screen bg-base-200 text-base-content">
      <header className="border-base-300 bg-base-100 border-b">
        <div className="mx-auto flex min-h-16 w-full max-w-7xl items-center justify-between px-5">
          <div className="flex items-center gap-3">
            <span className="bg-success text-success-content flex size-10 items-center justify-center rounded-lg">
              <ChefHat aria-hidden="true" size={22} />
            </span>
            <div>
              <p className="text-lg font-semibold">PantryPal AI</p>
              <p className="text-base-content/60 text-sm">Frontend workspace</p>
            </div>
          </div>
          <span className="badge badge-outline">React + DaisyUI</span>
        </div>
      </header>

      <section className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-5 py-10">
        <div className="max-w-3xl">
          <p className="text-success text-sm font-semibold uppercase">Scaffold ready</p>
          <h1 className="mt-3 text-4xl font-bold text-base-content">
            A three-panel pantry workspace is coming next.
          </h1>
          <p className="text-base-content/70 mt-4 max-w-2xl">
            This first frontend slice wires the React app, Tailwind, DaisyUI, and
            icons so the next commit can focus on the actual recommendation UI.
          </p>
        </div>

        <div className="grid gap-4 lg:grid-cols-3">
          <div className="border-base-300 bg-base-100 rounded-lg border p-5">
            <div className="mb-4 flex items-center gap-2 font-semibold">
              <ListChecks aria-hidden="true" size={20} />
              Pantry
            </div>
            <p className="text-base-content/65 text-sm">
              Ingredient entry and pantry state will live here.
            </p>
          </div>
          <div className="border-base-300 bg-base-100 rounded-lg border p-5">
            <div className="mb-4 flex items-center gap-2 font-semibold">
              <ChefHat aria-hidden="true" size={20} />
              Recipes
            </div>
            <p className="text-base-content/65 text-sm">
              Ranked recipe recommendations will appear in the center panel.
            </p>
          </div>
          <div className="border-base-300 bg-base-100 rounded-lg border p-5">
            <div className="mb-4 flex items-center gap-2 font-semibold">
              <Bot aria-hidden="true" size={20} />
              Assistant
            </div>
            <p className="text-base-content/65 text-sm">
              Cooking Q&A and retrieved recipe context will sit on the right.
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}

export default App
