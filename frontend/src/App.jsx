import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'

// Debounce hook for real-time AI insight
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  return debouncedValue;
}

const API_URL = "http://localhost:8000"; // Assuming Backend runs on port 8000

function App() {
  // State for form
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  // State for AI Insight
  const [prediction, setPrediction] = useState(null);
  const [loadingPrediction, setLoadingPrediction] = useState(false);

  // State for Tickets (Admin View)
  const [tickets, setTickets] = useState([]);

  // Debounced input for prediction
  const debouncedDescription = useDebounce(description, 500);
  const debouncedTitle = useDebounce(title, 500);

  // Fetch standard stats or mock tickets on mount
  useEffect(() => {
    // In a real app, we'd fetch tickets from backend. 
    // Here we'll start with some mock data for the Admin view.
    setTickets([
      { id: 101, title: 'Laptop won\'t turn on', category: 'Hardware', priority: 'High', status: 'Open' },
      { id: 102, title: 'Need access to Jira', category: 'Account Access', priority: 'Medium', status: 'Resolved' },
    ]);
  }, []);

  // Effect to trigger AI prediction
  useEffect(() => {
    if ((debouncedTitle || debouncedDescription) && (debouncedTitle.length > 3 || debouncedDescription.length > 5)) {
      fetchPrediction(debouncedTitle, debouncedDescription);
    } else {
      setPrediction(null);
    }
  }, [debouncedTitle, debouncedDescription]);

  const fetchPrediction = async (t, d) => {
    setLoadingPrediction(true);
    try {
      // In production, reliable error handling is key.
      const response = await axios.post(`${API_URL}/api/v1/tickets/analyze`, {
        title: t,
        description: d
      });
      setPrediction(response.data);
    } catch (error) {
      console.error("AI Service Error:", error);
      // Fallback or silent fail for live insight
    } finally {
      setLoadingPrediction(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title || !description) return;

    // Simulate submission
    const newTicket = {
      id: Math.floor(Math.random() * 1000) + 103, // Mock ID
      title,
      category: prediction?.category || 'Unassigned',
      priority: prediction?.priority || 'Low',
      status: 'New'
    };

    setTickets([newTicket, ...tickets]);

    // Reset Form
    setTitle('');
    setDescription('');
    setPrediction(null);

    // Notify user (simple alert for MVP, ideally a toast)
    // alert("Ticket Submitted Successfully!"); // User rule: no native alerts? Wait, rule was for previous user? 
    // Current user has no rule about alerts, but "no native alerts" is good practice.
    // We'll just rely on the UI updating.
  };

  const getPriorityColor = (p) => {
    switch (p) {
      case 'High': return 'bg-red-100 text-red-800';
      case 'Medium': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-green-100 text-green-800';
    }
  };

  return (
    <div className="min-h-screen bg-ibm-blue-10 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-ibm-blue-90">CogniSupport</h1>
        <p className="text-gray-600">AI-Driven IT Helpdesk Portal</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Submission Form */}
        <div className="lg:col-span-2 space-y-8">
          <section className="card">
            <h2 className="text-xl font-semibold mb-4 text-ibm-blue-80 flex items-center">
              Create New Ticket
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Issue Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="input-field"
                  placeholder="e.g., Cannot access VPN"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="input-field h-32 resize-none"
                  placeholder="Describe the issue in detail..."
                />
              </div>
              <div className="flex justify-end">
                <button type="submit" className="btn-primary">
                  Submit Ticket
                </button>
              </div>
            </form>
          </section>

          {/* Admin View Table */}
          <section className="card">
            <h2 className="text-xl font-semibold mb-4 text-ibm-blue-80">Recent Tickets (Admin View)</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-ibm-blue-10">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Issue</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {tickets.map((ticket) => (
                    <tr key={ticket.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{ticket.id}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-ibm-gray-100">{ticket.title}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ticket.category}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`badge ${getPriorityColor(ticket.priority)}`}>
                          {ticket.priority}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ticket.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </div>

        {/* Right Column: AI Live Insight */}
        <aside className="lg:col-span-1">
          <div className={`card sticky top-8 transition-all duration-300 ${prediction ? 'border-l-4 border-l-ibm-blue-50 ring-1 ring-ibm-blue-20' : ''}`}>
            <h2 className="text-xl font-semibold mb-4 text-ibm-blue-80 flex items-center">
              <svg className="w-5 h-5 mr-2 text-ibm-blue-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              AI Diagnostics
            </h2>

            {!title && !description ? (
              <div className="text-gray-400 italic text-center py-8">
                Start typing to see AI insights...
              </div>
            ) : loadingPrediction ? (
              <div className="animate-pulse space-y-4">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              </div>
            ) : prediction ? (
              <div className="space-y-4 animate-fadeIn">
                <div className="bg-ibm-blue-10 p-4 rounded-md">
                  <p className="text-xs text-gray-500 uppercase font-bold tracking-wide">Suggested Category</p>
                  <p className="text-lg font-bold text-ibm-blue-80 mt-1">{prediction.category}</p>
                </div>

                <div className="flex space-x-3">
                  <div className="flex-1 bg-ibm-blue-10 p-4 rounded-md">
                    <p className="text-xs text-gray-500 uppercase font-bold tracking-wide">Priority</p>
                    <div className={`mt-1 inline-block px-2 py-1 rounded text-sm font-bold ${prediction.priority === 'High' ? 'text-red-600 bg-red-50' :
                      prediction.priority === 'Medium' ? 'text-yellow-600 bg-yellow-50' :
                        'text-green-600 bg-green-50'
                      }`}>
                      {prediction.priority}
                    </div>
                  </div>
                  <div className="flex-1 bg-ibm-blue-10 p-4 rounded-md">
                    <p className="text-xs text-gray-500 uppercase font-bold tracking-wide">Confidence</p>
                    <p className="text-lg font-bold text-ibm-blue-80 mt-1">{prediction.confidence}</p>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-gray-100">
                  <p className="text-sm text-gray-500">
                    <span className="font-semibold text-ibm-blue-60">System Note:</span> Ticket will be auto-routed to the <strong>{prediction.category} Team</strong>.
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-gray-400 italic text-center py-8">
                Analyzing input...
              </div>
            )}
          </div>
        </aside>
      </div>
    </div>
  )
}

export default App
