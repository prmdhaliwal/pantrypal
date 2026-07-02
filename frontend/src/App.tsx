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

import {
  createPantryPalApi,
  type RecipeRecommendation,
  type RetrievedContext,
} from './api/pantryPalApi'

type ThemeMode = 'dark' | 'light' | 'system'
type AssistantStatus = 'idle' | 'loading' | 'loaded' | 'error'
type RecommendationStatus = 'idle' | 'loading' | 'loaded' | 'error'
type ResolvedTheme = 'pantrypal-dark' | 'pantrypal-light'

const starterIngredients = ['eggs', 'rice', 'tomato']

const sampleRecipes: RecipeRecommendation[] = [
  {
    id: 'sample-egg-fried-rice',
    name: 'Egg Fried Rice',
    imageUrl: null,
    category: 'Quick dinner',
    area: null,
    matchedIngredients: ['eggs', 'rice'],
    missingIngredients: ['soy sauce'],
    score: 0.67,
    instructionsUrl: null,
  },
  {
    id: 'sample-simple-omelette',
    name: 'Simple Omelette',
    imageUrl: null,
    category: 'Breakfast',
    area: null,
    matchedIngredients: ['eggs'],
    missingIngredients: ['cheese'],
    score: 0.5,
    instructionsUrl: null,
  },
  {
    id: 'sample-tomato-pasta',
    name: 'Tomato Pasta',
    imageUrl: null,
    category: 'Pantry staple',
    area: null,
    matchedIngredients: ['tomato'],
    missingIngredients: ['pasta', 'garlic'],
    score: 0.33,
    instructionsUrl: null,
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
  const pantryPalApi = useMemo(() => createPantryPalApi(), [])
  const [ingredients, setIngredients] = useState(starterIngredients)
  const [ingredientInput, setIngredientInput] = useState('')
  const [assistantAnswer, setAssistantAnswer] = useState('')
  const [assistantQuestion, setAssistantQuestion] = useState(
    'Can I make the fried rice without soy sauce?',
  )
  const [assistantStatus, setAssistantStatus] = useState<AssistantStatus>('idle')
  const [recommendations, setRecommendations] = useState<RecipeRecommendation[]>([])
  const [recommendationStatus, setRecommendationStatus] =
    useState<RecommendationStatus>('idle')
  const [retrievedContext, setRetrievedContext] = useState<RetrievedContext[]>([])
  const [selectedRecipeId, setSelectedRecipeId] = useState<string>()
  const [themeMode, setThemeMode] = useState<ThemeMode>('dark')
  const [systemTheme, setSystemTheme] = useState<ResolvedTheme>(getSystemTheme)

  const ingredientSummary = useMemo(
    () => `${ingredients.length} pantry items ready`,
    [ingredients.length],
  )
  const hasIngredients = ingredients.length > 0
  const resolvedTheme = themeMode === 'system' ? systemTheme : `pantrypal-${themeMode}`
  const displayedRecipes =
    recommendationStatus === 'loaded' ? recommendations : sampleRecipes
  const selectedRecipe = recommendations.find(
    (recipe) => recipe.id === selectedRecipeId,
  )
  const recommendationStatusText =
    recommendationStatus === 'loading'
      ? `Searching with ${ingredients.length} pantry items.`
      : 'Sample matches are shown. Run search to rank recipes from your pantry.'
  const assistantStatusText =
    assistantStatus === 'loading'
      ? `Retrieving recipe context for ${ingredients.length} pantry items.`
      : selectedRecipe
        ? `Using ${selectedRecipe.name} as recipe context.`
        : 'No recipe selected. The assistant will answer from your pantry list.'

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

    resetBackendState()
    setIngredients([...ingredients, nextIngredient])
    setIngredientInput('')
  }

  function removeIngredient(ingredient: string) {
    resetBackendState()
    setIngredients(ingredients.filter((item) => item !== ingredient))
  }

  function resetBackendState() {
    setAssistantAnswer('')
    setAssistantStatus('idle')
    setRecommendations([])
    setRecommendationStatus('idle')
    setRetrievedContext([])
    setSelectedRecipeId(undefined)
  }

  async function findRecommendations() {
    if (!hasIngredients) {
      return
    }

    setRecommendationStatus('loading')
    setSelectedRecipeId(undefined)

    try {
      const response = await pantryPalApi.recommendRecipes(ingredients)
      setRecommendations(response.results)
      setRecommendationStatus('loaded')
    } catch {
      setRecommendationStatus('error')
    }
  }

  async function askAssistant() {
    const question = assistantQuestion.trim()

    if (!question || !hasIngredients) {
      return
    }

    setAssistantStatus('loading')

    try {
      const response = await pantryPalApi.askCookingQuestion({
        question,
        ingredients,
        selectedRecipeId,
      })

      setAssistantAnswer(response.answer)
      setRetrievedContext(response.retrievedContext)
      setAssistantStatus('loaded')
    } catch {
      setAssistantStatus('error')
    }
  }

  return (
    <main
      className="min-h-screen bg-base-200 text-base-content"
      data-theme={resolvedTheme}
    >
      <header className="border-base-300 bg-base-100/95 border-b">
        <div className="mx-auto flex min-h-16 w-full max-w-7xl items-center justify-between gap-4 px-5">
          <div className="flex min-w-0 items-center gap-3">
            <span className="bg-success text-success-content flex size-10 shrink-0 items-center justify-center rounded-lg">
              <ChefHat aria-hidden="true" size={22} />
            </span>
            <div className="min-w-0">
              <p className="text-lg font-semibold">PantryPal AI</p>
              <p className="text-base-content/60 text-sm leading-tight">
                Ingredient-first recipe workspace
              </p>
            </div>
          </div>
          <div className="flex shrink-0 items-center gap-3">
            <div className="hidden items-center gap-2 text-sm md:flex">
              <span className="badge badge-success badge-outline">Pantry ready</span>
              <span className="badge badge-outline">Recipe context</span>
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
            <p className="text-success text-sm font-semibold uppercase">
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
                    className="badge badge-lg max-w-full gap-1 border-base-300 bg-base-200"
                    key={ingredient}
                  >
                    <span className="max-w-40 truncate">{ingredient}</span>
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

              {!hasIngredients && (
                <div className="alert alert-warning text-sm">
                  Your pantry is empty. Add an ingredient to unlock recipe search.
                </div>
              )}

              <div className="border-base-300 rounded-lg border p-4">
                <div className="mb-3 flex items-center gap-2 text-sm font-semibold">
                  <Sparkles aria-hidden="true" size={16} />
                  Recipe matching
                </div>
                <p className="text-base-content/65 text-sm">
                  Rank recipes by what you already have and what you still need.
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
                  Compare what you have against what each recipe needs.
                </p>
              </div>
              <button
                className="btn btn-warning"
                disabled={!hasIngredients || recommendationStatus === 'loading'}
                onClick={findRecommendations}
                type="button"
              >
                <Search aria-hidden="true" size={16} />
                {recommendationStatus === 'loading' ? 'Finding recipes' : 'Find recipes'}
              </button>
            </div>

            <div className="flex flex-col gap-4 p-5">
              {recommendationStatus !== 'loaded' && (
                <div
                  className={`alert text-sm ${
                    recommendationStatus === 'loading' ? 'alert-warning' : ''
                  }`}
                >
                  {recommendationStatusText}
                </div>
              )}

              {recommendationStatus === 'error' && (
                <div className="alert alert-error" role="alert">
                  Recipe search is unavailable. Make sure the backend is running,
                  then try again.
                </div>
              )}

              {recommendationStatus === 'loaded' && recommendations.length === 0 && (
                <div className="border-base-300 rounded-lg border p-4 text-sm">
                  No matches for this pantry yet. Add another ingredient or try a
                  broader pantry item.
                </div>
              )}

              <div className="grid gap-4 lg:grid-cols-3 xl:grid-cols-1 2xl:grid-cols-3">
                {displayedRecipes.map((recipe) => (
                  <article
                    className={`rounded-lg border bg-base-200/60 p-4 ${
                      recipe.id === selectedRecipeId
                        ? 'border-info'
                        : 'border-base-300'
                    }`}
                    key={recipe.id}
                  >
                    <div className="mb-4 flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <h3 className="break-words font-semibold">{recipe.name}</h3>
                        <p className="text-base-content/60 mt-1 text-sm">
                          Matched: {formatIngredientList(recipe.matchedIngredients)}
                        </p>
                      </div>
                      <span className="badge badge-warning badge-outline">
                        {formatScore(recipe.score)}
                      </span>
                    </div>
                    <div className="mb-4 flex items-center gap-2 text-sm">
                      <Clock3 aria-hidden="true" size={15} />
                      {recipe.category ?? recipe.area ?? 'Recipe match'}
                    </div>
                    <p className="text-base-content/65 break-words text-sm">
                      Missing: {formatIngredientList(recipe.missingIngredients)}
                    </p>
                    {recipe.id === selectedRecipeId && (
                      <span className="badge badge-info badge-outline mt-4">
                        Assistant context
                      </span>
                    )}
                    {recommendationStatus === 'loaded' && (
                      <button
                        aria-label={`Use ${recipe.name} in assistant`}
                        aria-pressed={recipe.id === selectedRecipeId}
                        className={`btn btn-xs mt-4 ${
                          recipe.id === selectedRecipeId
                            ? 'btn-info'
                            : 'btn-outline'
                        }`}
                        onClick={() => setSelectedRecipeId(recipe.id)}
                        type="button"
                      >
                        {recipe.id === selectedRecipeId
                          ? 'Selected'
                          : 'Ask about this'}
                      </button>
                    )}
                  </article>
                ))}
              </div>
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
              {selectedRecipe && (
                <p className="badge badge-info badge-outline h-auto max-w-full justify-start whitespace-normal">
                  Selected recipe: {selectedRecipe.name}
                </p>
              )}

              <div
                className={`alert text-sm ${
                  assistantStatus === 'loading' ? 'alert-info' : ''
                }`}
              >
                {assistantStatusText}
              </div>

              <label className="form-control">
                <span className="label-text mb-2">Question</span>
                <textarea
                  className="textarea textarea-bordered min-h-28 resize-none"
                  onChange={(event) => setAssistantQuestion(event.target.value)}
                  value={assistantQuestion}
                />
              </label>

              <button
                className="btn btn-info"
                disabled={!hasIngredients || assistantStatus === 'loading'}
                onClick={askAssistant}
                type="button"
              >
                <MessageSquareText aria-hidden="true" size={16} />
                {assistantStatus === 'loading' ? 'Asking assistant' : 'Ask assistant'}
              </button>

              {assistantStatus === 'error' && (
                <div className="alert alert-error" role="alert">
                  Assistant is unavailable. Make sure the backend is running, then
                  try again.
                </div>
              )}

              <div className="border-base-300 rounded-lg border p-4">
                <p className="mb-2 text-sm font-semibold">Recipe context</p>
                {retrievedContext.length > 0 ? (
                  <div className="space-y-3">
                    {retrievedContext.map((context) => (
                      <div key={context.recipeId}>
                        <div className="mb-1 flex items-center justify-between gap-2">
                          <p className="break-words text-sm font-medium">
                            {context.name}
                          </p>
                          <span className="badge badge-info badge-outline">
                            {formatScore(context.score)}
                          </span>
                        </div>
                        <p className="text-base-content/65 break-words text-sm">
                          {context.text}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-base-content/65 text-sm">
                    Ask a question to see the recipe context behind the answer.
                  </p>
                )}
              </div>

              <div className="chat chat-start mt-auto">
                <div className="chat-bubble bg-base-200 text-base-content break-words">
                  {assistantAnswer ||
                    'Your answer will appear here after the assistant checks recipe context.'}
                </div>
              </div>
            </div>
          </section>
        </div>
      </section>
    </main>
  )
}

function formatIngredientList(ingredients: string[]) {
  return ingredients.length > 0 ? ingredients.join(', ') : 'none'
}

function formatScore(score: number) {
  return `${Math.round(score * 100)}%`
}

export default App
