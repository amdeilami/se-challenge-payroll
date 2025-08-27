import { useState } from 'react'
import { uploadTimesheet, fetchPayroll } from './lib/api'
import './App.css'


export default function App() {
  // Upload state
  const [file, setFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState('idle') // idle | loading | ok | error
  const [uploadMsg, setUploadMsg] = useState('')

  // Report state
  const today = new Date().toISOString().slice(0, 10)
  const [start, setStart] = useState('2023-01-01')
  const [end, setEnd] = useState(today)
  const [reportStatus, setReportStatus] = useState('idle') // idle | loading | ok | error
  const [report, setReport] = useState(null)
  const [reportErr, setReportErr] = useState('')

  async function onUpload(e) {
    e.preventDefault()
    if (!file) {
      setUploadStatus('error')
      setUploadMsg('Please choose a CSV file first.')
      return
    }
    setUploadStatus('loading')
    setUploadMsg('')
    try {
      const res = await uploadTimesheet(file)
      setUploadStatus('ok')
      setUploadMsg(typeof res === 'string' ? res : 'Upload successful.')
    } catch (err) {
      setUploadStatus('error')
      setUploadMsg(err.message || String(err))
    }
  }

  async function onFetchReport(e) {
    e.preventDefault()
    if (!start || !end) {
      setReportStatus('error')
      setReportErr('Please set both start and end dates.')
      return
    }
    if (new Date(start) > new Date(end)) {
      setReportStatus('error')
      setReportErr('Start date must be before end date.')
      return
    }
    setReportStatus('loading')
    setReportErr('')
    setReport(null)
    try {
      const data = await fetchPayroll({ start, end })
      setReport(data)
      setReportStatus('ok')
    } catch (err) {
      setReportStatus('error')
      setReportErr(err.message || String(err))
    }
  }

  function downloadReport() {
    if (!report) return
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `payroll_${start}_to_${end}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className='root' /*style={{ maxWidth: 1080, margin: '16px auto', padding: '16px' }}*/>
      <h1 style={{textAlign: 'center'}}>Wave Demo</h1>

      {/* Upload CSV */}
      <section className="card">
        <h2 style={{ marginTop: 0, marginBottom: 32, textAlign: 'center' }}> Upload your CSV file</h2>
        <form onSubmit={onUpload} style={{maxWidth: 150, margin: '0 auto'}}>
          <input
            type="file"
            accept=".csv,text/csv"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: 16}}>
            <button type="submit" disabled={uploadStatus === 'loading'}>
              {uploadStatus === 'loading' ? 'Uploading…' : 'Submit'}
            </button>
          </div>
        </form>
        {uploadStatus === 'ok' && <p style={{ color: 'green' }}>{uploadMsg}</p>}
        {uploadStatus === 'error' && <p style={{ color: 'red' }}>{uploadMsg}</p>}
      </section>

      {/* Fetch Report */}
      <section className="card">
        <h2 style={{ marginTop: 0, marginBottom: 32, textAlign: 'center' }}> Fetch Payroll Report</h2>
        <form onSubmit={onFetchReport} style={{ display: 'grid', gap: 12, maxWidth: 200,  margin: '0 auto' }}>
          <label>
            Start date:
            <input type="date" value={start} onChange={(e) => setStart(e.target.value)} />
          </label>
          <label>
            End date:
            <input type="date" value={end} onChange={(e) => setEnd(e.target.value)} />
          </label>
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: 16}}>
            <button type="submit" disabled={reportStatus === 'loading'}>
              {reportStatus === 'loading' ? 'Loading…' : 'Get report'}
            </button>
            <button
              type="button"
              onClick={downloadReport}
              disabled={!report}
              style={{ marginLeft: 8 }}
            >
              Download JSON
            </button>
          </div>
        </form>

        {reportStatus === 'error' && <p style={{ color: 'crimson' }}>{reportErr}</p>}

        {report && (
          <>
            <h3>Report (JSON)</h3>
            <pre className='pre'>{JSON.stringify(report, null, 2)}</pre>
          </>
        )}
      </section>
    </div>
  )
}