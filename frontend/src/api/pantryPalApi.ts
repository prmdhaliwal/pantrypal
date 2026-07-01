export type RecipeRecommendation = {
  id: string
  name: string
  imageUrl: string | null
  category: string | null
  area: string | null
  matchedIngredients: string[]
  missingIngredients: string[]
  score: number
  instructionsUrl: string | null
}

export type RecommendResponse = {
  results: RecipeRecommendation[]
}

export type AskCitation = {
  recipeId: string
  name: string
}

export type RetrievedContext = {
  recipeId: string
  name: string
  text: string
  score: number
}

export type AskRequest = {
  question: string
  ingredients: string[]
  selectedRecipeId?: string
}

export type AskResponse = {
  answer: string
  citations: AskCitation[]
  retrievedContext: RetrievedContext[]
  providerConfigured: boolean
}

type ApiFetch = (input: string, init?: RequestInit) => Promise<Response>

type PantryPalApiOptions = {
  baseUrl?: string
  fetcher?: ApiFetch
}

export class PantryPalApiError extends Error {
  status: number

  constructor(status: number) {
    super(`PantryPal API request failed with status ${status}`)
    this.name = 'PantryPalApiError'
    this.status = status
  }
}

const DEFAULT_API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export function createPantryPalApi(options: PantryPalApiOptions = {}) {
  const baseUrl = trimTrailingSlash(options.baseUrl ?? DEFAULT_API_BASE_URL)
  const fetcher = options.fetcher ?? fetch

  return {
    recommendRecipes(ingredients: string[]) {
      return postJson<RecommendResponse>(fetcher, `${baseUrl}/recommend`, {
        ingredients,
      })
    },
    askCookingQuestion(request: AskRequest) {
      return postJson<AskResponse>(fetcher, `${baseUrl}/ask`, request)
    },
  }
}

function trimTrailingSlash(value: string) {
  return value.replace(/\/$/, '')
}

async function postJson<ResponseBody>(
  fetcher: ApiFetch,
  url: string,
  body: unknown,
) {
  const response = await fetcher(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  })

  if (!response.ok) {
    throw new PantryPalApiError(response.status)
  }

  return response.json() as Promise<ResponseBody>
}
