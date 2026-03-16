import React, { useEffect, useMemo, useState } from 'react';

const baseUrl = process.env.REACT_APP_CODESPACE_NAME
  ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api`
  : 'http://localhost:8000/api';

const formatValue = (value) => {
  if (value === null || value === undefined) return '';
  if (typeof value === 'object') return JSON.stringify(value);
  return value.toString();
};

const buildTable = (data) => {
  if (!Array.isArray(data) || data.length === 0) {
    return <p className="text-muted">No items to display.</p>;
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="table-responsive">
      <table className="table table-striped table-bordered table-hover">
        <thead className="table-light">
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={`${idx}-${col}`}>{formatValue(row[col])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const Users = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showRaw, setShowRaw] = useState(false);

  const endpoint = `${baseUrl}/users/`;

  useEffect(() => {
    console.log('[Users] fetching from', endpoint);

    fetch(endpoint)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
      })
      .then((json) => {
        console.log('[Users] response', json);
        const results = Array.isArray(json) ? json : json?.results ?? [];
        setData(results);
      })
      .catch((err) => {
        console.error('[Users] fetch error', err);
        setError(err.message || 'Unknown error');
      })
      .finally(() => {
        setLoading(false);
      });
  }, [endpoint]);

  const table = useMemo(() => buildTable(data), [data]);

  return (
    <div className="container py-4">
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <h2 className="mb-0 page-title">Users</h2>
          <button
            type="button"
            className="btn btn-sm btn-outline-primary"
            onClick={() => setShowRaw(true)}
          >
            View JSON
          </button>
        </div>
        <div className="card-body">
          {loading && <div className="spinner-border" role="status"><span className="visually-hidden">Loading...</span></div>}
          {error && <div className="alert alert-danger">Error: {error}</div>}
          {!loading && !error && (
            <>
              <p className="text-muted">Fetched {data.length} items.</p>
              {table}
            </>
          )}
        </div>
      </div>

      {showRaw && (
        <div className="modal fade show" style={{ display: 'block' }} tabIndex={-1}>
          <div className="modal-dialog modal-xl">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Users JSON</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setShowRaw(false)}
                />
              </div>
              <div className="modal-body">
                <pre style={{ maxHeight: 400, overflow: 'auto' }}>
                  {JSON.stringify(data, null, 2)}
                </pre>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => setShowRaw(false)}
                >
                  Close
                </button>
              </div>
            </div>
          </div>
          <div className="modal-backdrop fade show" onClick={() => setShowRaw(false)} />
        </div>
      )}
    </div>
  );
};

export default Users;
