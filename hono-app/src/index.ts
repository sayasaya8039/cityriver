import { Hono } from 'hono'
import { home } from './routes/home'
import { services } from './routes/services'
import { products } from './routes/products'
import { terms } from './routes/terms'

const app = new Hono()
  .route('/', home)
  .route('/', services)
  .route('/', products)
  .route('/', terms)

export type AppType = typeof app
export default app
