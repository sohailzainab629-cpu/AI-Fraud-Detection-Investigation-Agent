
import { useEffect, useState } from 'react'
import sampleTransaction from './sampleTransaction'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [health, setHealth] = useState(null)
  const [reviews, setReviews] = useState([])
  const [transaction, setTransaction] = useState(sampleTransaction)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [updatingReview, setUpdatingReview] = useState(null)

  const loadDashboard = async () => {
    try {
      const healthResponse = await fetch(`${API_URL}/health`)
      if (!healthResponse.ok) throw new Error('Health check failed')
      setHealth(await healthResponse.json())

      const reviewsResponse = await fetch(`${API_URL}/reviews`)
      if (!reviewsResponse.ok) throw new Error('Reviews could not load')

      const reviewsData = await reviewsResponse.json()
      setReviews(reviewsData.reviews || [])
    } catch (err) {
      setError('Backend connection error. Check your server.')
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  const investigateTransaction = async () => {
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/investigate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(transaction),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          typeof data.detail === 'string'
            ? data.detail
            : JSON.stringify(data.detail || data)
        )
      }

      setResult(data)
      await loadDashboard()
    } catch (err) {
      setError(err.message || 'Investigation failed.')
    } finally {
      setLoading(false)
    }
  }

  const submitDecision = async (reviewId, decision) => {
    setUpdatingReview(reviewId)
    setError('')

    try {
      const response = await fetch(
        `${API_URL}/reviews/${reviewId}/decision`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ decision }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Decision could not be saved')
      }

      await loadDashboard()
    } catch (err) {
      setError(err.message || 'Review update failed.')
    } finally {
      setUpdatingReview(null)
    }
  }

  const pendingReviews = reviews.filter(
    (review) => review.status === 'Pending'
  )

  const reviewedReviews = reviews.filter(
    (review) => review.status === 'Reviewed'
  )

  const highRiskReviews = reviews.filter(
    (review) => (review.risk_level || review.risk) === 'High'
  )

  const mediumRiskReviews = reviews.filter(
    (review) => (review.risk_level || review.risk) === 'Medium'
  )

  const lowRiskReviews = reviews.filter(
    (review) => (review.risk_level || review.risk) === 'Low'
  )

  const analytics = [
    { label: 'High Risk', count: highRiskReviews.length, color: 'bg-red-500' },
    { label: 'Medium Risk', count: mediumRiskReviews.length, color: 'bg-yellow-500' },
    { label: 'Low Risk', count: lowRiskReviews.length, color: 'bg-green-500' },
  ]

  const maxRiskCount = Math.max(
    1,
    ...analytics.map((item) => item.count)
  )

  return (
    <div className="flex min-h-screen bg-slate-950 text-white">

      {/* SIDEBAR */}
      <aside className="min-h-screen w-64 shrink-0 border-r border-slate-800 bg-slate-900 p-6">
        <h1 className="text-2xl font-bold text-blue-400">
          FraudGuard AI
        </h1>

        <p className="mt-2 text-sm text-slate-400">
          Enterprise Fraud Detection
        </p>

        <nav className="mt-10 space-y-4 text-slate-300">
          <a href="#dashboard" className="block rounded-lg bg-blue-600 p-3 text-white">
            Dashboard
          </a>
          <a href="#investigation" className="block rounded-lg p-3 hover:bg-slate-800">
            Transaction Investigation
          </a>
          <a href="#reviews" className="block rounded-lg p-3 hover:bg-slate-800">
            Human Reviews
          </a>
          <a href="#analytics" className="block rounded-lg p-3 hover:bg-slate-800">
            Analytics
          </a>
        </nav>
      </aside>

      {/* MAIN CONTENT */}
      <main className="min-w-0 flex-1 p-8">

        <div id="dashboard" className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-3xl font-bold">
              Fraud Detection Dashboard
            </h2>
            <p className="mt-2 text-slate-400">
              AI-powered transaction monitoring and investigation
            </p>
          </div>

          <button
            onClick={loadDashboard}
            className="rounded-lg bg-blue-600 px-5 py-3 hover:bg-blue-700"
          >
            Refresh Dashboard
          </button>
        </div>

        {error && (
          <p className="mt-5 rounded-lg bg-red-900/30 p-4 text-red-300">
            {error}
          </p>
        )}

        {/* STATISTICS */}
        <div className="mt-8 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
          <StatCard
            title="Backend Status"
            value={health?.model_loaded ? 'Online' : 'Offline'}
          />
          <StatCard title="Dataset Transactions" value="283,726" />
          <StatCard title="Model Accuracy" value="99.95%" />
          <StatCard title="Pending Reviews" value={pendingReviews.length} />
        </div>

        {/* INVESTIGATION */}
        <section
          id="investigation"
          className="mt-10 rounded-xl border border-slate-800 bg-slate-900 p-6"
        >
          <h2 className="text-xl font-bold">
            Transaction Investigation
          </h2>

          <p className="mt-2 text-sm text-slate-400">
            Load a dataset transaction and run the AI investigation agent.
          </p>

          <div className="mt-6 flex flex-wrap gap-4">
            <button
              onClick={() => {
                setTransaction(sampleTransaction)
                setResult(null)
                setError('')
              }}
              className="rounded-lg border border-blue-500 px-5 py-3 text-blue-400 hover:bg-blue-500/10"
            >
              Load Sample Transaction
            </button>

            <button
              onClick={investigateTransaction}
              disabled={loading}
              className="rounded-lg bg-blue-600 px-5 py-3 font-semibold hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Investigating...' : 'Investigate Transaction'}
            </button>
          </div>

          {result && (
            <div className="mt-8 rounded-xl border border-slate-700 bg-slate-950 p-6">
              <h3 className="text-xl font-bold text-green-400">
                Investigation Result
              </h3>

              <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <StatCard
                  title="Prediction"
                  value={result.result}
                />
                <StatCard
                  title="Fraud Probability"
                  value={`${(result.fraud_probability * 100).toFixed(2)}%`}
                />
                <StatCard
                  title="Risk Level"
                  value={result.risk_level}
                />
                <StatCard
                  title="Recommendation"
                  value={result.recommendation}
                />
              </div>

              <div className="mt-6">
                <h4 className="mb-3 font-semibold">AI Investigation Report</h4>
                <pre className="overflow-x-auto whitespace-pre-wrap rounded-lg bg-slate-900 p-5 text-sm leading-6 text-slate-300">
                  {result.investigation_report}
                </pre>
              </div>

              {result.human_review && (
                <p className="mt-4 rounded-lg bg-yellow-900/30 p-4 text-yellow-300">
                  Human review created: {result.human_review.review_id}
                </p>
              )}

              {!result.human_review && result.risk_level !== 'High' && (
                <p className="mt-4 text-sm text-slate-400">
                  No automatic human review was created because this transaction
                  did not receive a High risk classification.
                </p>
              )}
            </div>
          )}
        </section>

        {/* HUMAN REVIEW */}
        <section
          id="reviews"
          className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6"
        >
          <h2 className="text-xl font-bold">
            Human Review Queue
          </h2>

          <p className="mt-2 text-slate-400">
            Pending transactions: {pendingReviews.length}
          </p>

          <div className="mt-5 space-y-4">
            {reviews.length === 0 ? (
              <p className="text-slate-400">No reviews available.</p>
            ) : (
              reviews.map((review) => (
                <div
                  key={review.review_id}
                  className="rounded-lg border border-slate-700 p-5"
                >
                  <p className="font-semibold">
                    Review ID: {review.review_id}
                  </p>

                  <p className="mt-2 text-sm text-slate-400">
                    Risk: {review.risk_level || review.risk || 'N/A'}
                    {' | '}
                    Amount: {review.amount ?? 'N/A'}
                    {' | '}
                    Status: {review.status}
                  </p>

                  {review.status === 'Pending' ? (
                    <div className="mt-4 flex flex-wrap gap-3">
                      <button
                        onClick={() => submitDecision(review.review_id, 'Approve')}
                        disabled={updatingReview === review.review_id}
                        className="rounded-lg bg-green-600 px-5 py-2 font-semibold hover:bg-green-700 disabled:opacity-50"
                      >
                        {updatingReview === review.review_id ? 'Saving...' : 'Approve'}
                      </button>

                      <button
                        onClick={() => submitDecision(review.review_id, 'Reject')}
                        disabled={updatingReview === review.review_id}
                        className="rounded-lg bg-red-600 px-5 py-2 font-semibold hover:bg-red-700 disabled:opacity-50"
                      >
                        Reject
                      </button>
                    </div>
                  ) : (
                    <p className="mt-3 text-sm text-green-400">
                      Decision: {review.decision || 'Reviewed'}
                    </p>
                  )}
                </div>
              ))
            )}
          </div>
        </section>

        {/* ANALYTICS */}
        <section
          id="analytics"
          className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6"
        >
          <h2 className="text-xl font-bold">Fraud Analytics</h2>
          <p className="mt-2 text-sm text-slate-400">
            Risk distribution based on recorded human review transactions.
          </p>

          <div className="mt-6 grid gap-4 sm:grid-cols-3">
            <StatCard title="Total Reviews" value={reviews.length} />
            <StatCard title="Pending" value={pendingReviews.length} />
            <StatCard title="Reviewed" value={reviewedReviews.length} />
          </div>

          <div className="mt-8 space-y-6">
            {analytics.map((item) => (
              <div key={item.label}>
                <div className="mb-2 flex justify-between">
                  <span>{item.label}</span>
                  <span className="text-slate-400">{item.count}</span>
                </div>

                <div className="h-3 overflow-hidden rounded-full bg-slate-800">
                  <div
                    className={`h-full rounded-full ${item.color}`}
                    style={{
                      width: `${(item.count / maxRiskCount) * 100}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          <p className="mt-6 text-xs text-slate-500">
            These charts summarize saved human review records, not all dataset transactions.
          </p>
        </section>

        <footer className="mt-10 border-t border-slate-800 py-6 text-center text-sm text-slate-500">
          FraudGuard AI | Enterprise AI Fraud Detection & Investigation Agent
        </footer>

      </main>
    </div>
  )
}

function StatCard({ title, value }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
      <p className="text-sm text-slate-400">{title}</p>
      <h3 className="mt-3 break-words text-2xl font-bold">{value}</h3>
    </div>
  )
}

export default App
