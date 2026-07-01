import { useEffect, useMemo, useState } from 'react'
import {
  Bot,
  ChefHat,
  Clock3,
  ListChecks,
  MessageSquareText,
  Monitor,
  Moon,
  Plus,
  Search,
  Sparkles,
  Sun,
  X,
} from 'lucide-react'

type ThemeMode = 'dark' | 'light' | 'system'
type ResolvedTheme = 'pantrypal-dark' | 'pantrypal-light'

const starterIngredients = ['eggs', 'rice', 'tomato']

const sampleRecipes = [
  {
    name: 'Egg Fried Rice',
    match: '2 of 3 ingredients',
    missing: 'soy sauce',
    score: '67%',
    tag: 'Quick dinner',
  },
  {
    name: 'Simple Omelette',
    match: '1 of 2 ingredients',
    missing: 'cheese',
    score: '50%',
    tag: 'Breakfast',
  },
  {
    name: 'Tomato Pasta',
    match: '1 of 3 ingredients',
    missing: 'pasta, garlic',
    score: '33%',
    tag: 'Pantry staple',
  },
]

function getSystemTheme(): ResolvedTheme {
  if (typeof window === 'undefined' || !window.matchMedia) {
    return 'pantrypal-dark'
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'pantrypal-dark'
    : 'pantrypal-light'
}

function App() {
  const [ingredients, setIngredients] = useState(starterIngredients)
  const [ingredientInput, setIngredientInput] = useState('')
  const [themeMode, setThemeMode] = useState<ThemeMode>('dark')
  const [systemTheme, setSystemTheme] = useState<ResolvedTheme>(getSystemTheme)

  const ingredientSummary = useMemo(
    () => `${ingredients.length} pantry items ready`,
    [ingredients.length],
  )
  const resolvedTheme = themeMode === 'system' ? systemTheme : `pantrypal-${themeMode}`

  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) {
      return undefined
    }

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const updateSystemTheme = () => setSystemTheme(getSystemTheme())

    updateSystemTheme()
    mediaQuery.addEventListener('change', updateSystemTheme)

    return () => mediaQuery.removeEventListener('change', updateSystemTheme)
  }, [])

  function addIngredient(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const nextIngredient = ingredientInput.trim().toLowerCase()

    if (!nextIngredient || ingredients.includes(nextIngredient)) {
      setIngredientInput('')
      return
    }

    setIngredients([...ingredients, nextIngredient])
    setIngredientInput('')
  }

  function removeIngredient(ingredient: string) {
    setIngredients(ingredients.filter((item) => item !== ingredient))
  }

  return (
    <main
      className="min-h-screen bg-base-200 text-base-content"
      data-theme={resolvedTheme}
    >
      <header className="border-base-300 bg-base-100/95 border-b">
        <div className="mx-auto flex min-h-16 w-full max-w-7xl items-center justify-between gap-4 px-5">
          <div className="flex items-center gap-3">
            <span className="bg-success text-success-content flex size-10 shrink-0 items-center justify-center rounded-lg">
              <ChefHat aria-hidden="true" size={22} />
            </span>
            <div>
              <p className="text-lg font-semibold">PantryPal AI</p>
              <p className="text-base-content/60 text-sm">
                Ingredient-first recipe workspace
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden items-center gap-2 text-sm md:flex">
              <span className="badge badge-success badge-outline">Local pantry</span>
              <span className="badge badge-outline">RAG assistant ready</span>
            </div>
            <div aria-label="Theme mode" className="join" role="group">
              <button
                aria-label="Use dark theme"
                aria-pressed={themeMode === 'dark'}
                className={`btn btn-square btn-sm join-item ${
                  themeMode === 'dark' ? 'btn-active' : ''
                }`}
                onClick={() => setThemeMode('dark')}
                title="Dark"
                type="button"
              >
                <Moon aria-hidden="true" size={16} />
              </button>
              <button
                aria-label="Use light theme"
                aria-pressed={themeMode === 'light'}
                className={`btn btn-square btn-sm join-item ${
                  themeMode === 'light' ? 'btn-active' : ''
                }`}
                onClick={() => setThemeMode('light')}
                title="Light"
                type="button"
              >
                <Sun aria-hidden="true" size={16} />
              </button>
              <button
                aria-label="Follow system theme"
                aria-pressed={themeMode === 'system'}
                className={`btn btn-square btn-sm join-item ${
                  themeMode === 'system' ? 'btn-active' : ''
                }`}
                onClick={() => setThemeMode('system')}
                title="System"
                type="button"
              >
                <Monitor aria-hidden="true" size={16} />
              </button>
            </div>
          </div>
        </div>
      </header>

      <section className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-5 py-6">
        <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
          <div>
            <p className="text-success text-sm font-semibold uppercase tracking-wide">
              Pantry workspace
            </p>
            <h1 className="mt-2 text-3xl font-bold text-base-content md:text-4xl">
              Turn what you have into dinner options.
            </h1>
            <p className="text-base-content/70 mt-3 max-w-2xl">
              Add pantry ingredients, compare recipe matches, then ask a grounded
              cooking question from the same workspace.
            </p>
          </div>
          <div className="stats border-base-300 bg-base-100 border shadow-none">
            <div className="stat min-w-44">
              <div className="stat-title">Pantry</div>
              <div className="stat-value text-2xl">{ingredients.length}</div>
              <div className="stat-desc">items entered</div>
            </div>
          </div>
        </div>

        <div className="grid min-h-[650px] gap-4 xl:grid-cols-[300px_minmax(0,1fr)_340px]">
          <section className="border-base-300 bg-base-100 flex flex-col rounded-lg border">
            <div className="border-base-300 border-b p-5">
              <div className="mb-2 flex items-center gap-2">
                <ListChecks aria-hidden="true" className="text-success" size={20} />
                <h2 className="text-xl font-semibold">Your pantry</h2>
              </div>
              <p className="text-base-content/65 text-sm">{ingredientSummary}</p>
            </div>

            <div className="flex flex-1 flex-col gap-5 p-5">
              <form className="join w-full" onSubmit={addIngredient}>
                <label className="sr-only" htmlFor="ingredient-input">
                  Add ingredient
                </label>
                <input
                  className="input join-item input-bordered min-w-0 flex-1"
                  id="ingredient-input"
                  onChange={(event) => setIngredientInput(event.target.value)}
                  placeholder="Add ingredient"
                  value={ingredientInput}
                />
                <button className="btn btn-success join-item" type="submit">
                  <Plus aria-hidden="true" size={16} />
                  Add
                </button>
              </form>

              <div className="flex flex-wrap gap-2">
                {ingredients.map((ingredient) => (
                  <span
                    className="badge badge-lg gap-1 border-base-300 bg-base-200"
                    key={ingredient}
                  >
                    {ingredient}
                    <button
                      aria-label={`Remove ${ingredient}`}
                      className="btn btn-ghost btn-xs btn-circle"
                      onClick={() => removeIngredient(ingredient)}
                      type="button"
                    >
                      <X aria-hidden="true" size={12} />
                    </button>
                  </span>
                ))}
              </div>

              <div className="border-base-300 mt-auto rounded-lg border p-4">
                <div className="mb-3 flex items-center gap-2 text-sm font-semibold">
                  <Sparkles aria-hidden="true" size={16} />
                  Smart matching
                </div>
                <p className="text-base-content/65 text-sm">
                  The next slice will send these ingredients to the backend
                  recommender and replace the sample recipes.
                </p>
              </div>
            </div>
          </section>

          <section className="border-base-300 bg-base-100 flex flex-col rounded-lg border">
            <div className="border-base-300 flex flex-col gap-4 border-b p-5 md:flex-row md:items-center md:justify-between">
              <div>
                <div className="mb-2 flex items-center gap-2">
                  <ChefHat aria-hidden="true" className="text-warning" size={20} />
                  <h2 className="text-xl font-semibold">Recipe recommendations</h2>
                </div>
                <p className="text-base-content/65 text-sm">
                  Ranked examples using the current pantry shape.
                </p>
              </div>
              <button className="btn btn-warning" type="button">
                <Search aria-hidden="true" size={16} />
                Find recipes
              </button>
            </div>

            <div className="grid gap-4 p-5 lg:grid-cols-3 xl:grid-cols-1 2xl:grid-cols-3">
              {sampleRecipes.map((recipe) => (
                <article
                  className="border-base-300 rounded-lg border bg-base-200/60 p-4"
                  key={recipe.name}
                >
                  <div className="mb-4 flex items-start justify-between gap-3">
                    <div>
                      <h3 className="font-semibold">{recipe.name}</h3>
                      <p className="text-base-content/60 mt-1 text-sm">
                        {recipe.match}
                      </p>
                    </div>
                    <span className="badge badge-warning badge-outline">
                      {recipe.score}
                    </span>
                  </div>
                  <div className="mb-4 flex items-center gap-2 text-sm">
                    <Clock3 aria-hidden="true" size={15} />
                    {recipe.tag}
                  </div>
                  <p className="text-base-content/65 text-sm">
                    Missing: {recipe.missing}
                  </p>
                </article>
              ))}
            </div>
          </section>

          <section className="border-base-300 bg-base-100 flex flex-col rounded-lg border">
            <div className="border-base-300 border-b p-5">
              <div className="mb-2 flex items-center gap-2">
                <Bot aria-hidden="true" className="text-info" size={20} />
                <h2 className="text-xl font-semibold">Cooking assistant</h2>
              </div>
              <p className="text-base-content/65 text-sm">
                Ask about a selected recipe or pantry substitution.
              </p>
            </div>

            <div className="flex flex-1 flex-col gap-5 p-5">
              <label className="form-control">
                <span className="label-text mb-2">Question</span>
                <textarea
                  className="textarea textarea-bordered min-h-28 resize-none"
                  defaultValue="Can I make the fried rice without soy sauce?"
                />
              </label>

              <button className="btn btn-info" type="button">
                <MessageSquareText aria-hidden="true" size={16} />
                Ask assistant
              </button>

              <div className="border-base-300 rounded-lg border p-4">
                <p className="mb-2 text-sm font-semibold">Retrieved context</p>
                <p className="text-base-content/65 text-sm">
                  Egg Fried Rice uses eggs and rice from your pantry. Soy sauce is
                  currently marked as missing.
                </p>
              </div>

              <div className="chat chat-start mt-auto">
                <div className="chat-bubble bg-base-200 text-base-content">
                  I will use recipe context here once the assistant panel is wired
                  to the backend.
                </div>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  )
}

export default App
