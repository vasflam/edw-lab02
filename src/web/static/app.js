'use strict';

const e = React.createElement;
const { useState } = React;
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  headers: {
    'ContentType': 'application/json',
  },
});

function SearchButton({ text, setLoading, loading, updateRows }) {
  const [enabled, setEnabled] = useState(true);
  const click = async (e) => {
    if (enabled) {
      setEnabled(false);
      setLoading(true);
      try {
        const response = await api.post('/search', {text});
        updateRows(response.data.items)
      } catch(e) {
      }
      setEnabled(true);
      setLoading(false);
    }
  }

  const classes = ["btn", "btn-primary", "btn-lg", "px-4", "gap-3", "m-2"];
  if (!enabled) {
    classes.push("disabled");
  }
  return (
    <button onClick={click} type="button" className={classes.join(' ')}>Search</button>
  )
}

function CancelButton({ handleClick }) {
  return (
    <button onClick={handleClick} type="button" class="btn btn-outline-secondary btn-lg px-4 m-2">Clear</button>
  )
}

function Spinner() {
  return (
    <div class="spinner-border text-primary" role="status">
      <span class="sr-only">Loading...</span>
    </div>
  )
}

function ResultTable({ rows, minimalScore }) {
  console.log(rows);
  const items = rows.filter(row => row.score >= minimalScore)
  console.log('minimalScore', minimalScore);
  console.log(items);
  return (
    <table class="table">
      <thead>
        <th>site</th>
        <th>link</th>
        <th>title</th>
        <th>percentage</th>
      </thead>
      <tbody>
        {items.map(item => {
          return (<tr key={item.link}>
            <td>{item.site}</td>
            <td>{item.link}</td>
            <td>{item.title}</td>
            <td>{item.score}</td>
          </tr>)
        })}
      </tbody>
    </table>
  )
}

function App() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false)
  const [rows, setRows] = useState([]);
  const [minimalScore, setMinimalScore] = useState(38);

  const handleChange = (e) => {
    setText(e.target.value)
  };

  const handleClick = () => {
    setText('');
  };

  const updateRows = (rows) => {
    if (Array.isArray(rows) && rows.length > 0) {
      setRows(rows);
    }
  };

  const minimalScoreOnChange = (e) => {
    setMinimalScore(e.target.value);
  };

  return (
    <div class="px-4 py-5 my-5 text-center">
      <h1 class="display-5 fw-bold">Check text uniqueness</h1>
      <div class="col-lg-6 mx-auto">
        <form>
          <div class="form-group">
            <textarea onChange={handleChange} placeholder="Enter text..." class="form-control" id="search-text" rows="5" value={text}></textarea>
          </div>
          <div class="form-row">
            <div class="form-group col-md-2">
              <label for="minimal-score">Minimal score</label>
              <div class="input-group">
                <input id="minimal-score" class="form-control" type="text" value={minimalScore} onChange={minimalScoreOnChange}/>
                <div class="input-group-append">
                  <div class="input-group-text">%</div>
                </div>
              </div>
            </div>
          </div>
          <div class="form-group">
            <div class="d-grid gap-2 d-sm-flex justify-content-sm-center">
              <SearchButton {...{text, setLoading, loading, updateRows }} />
              <CancelButton handleClick={handleClick} minimalScore={minimalScore}/>
            </div>
          </div>
        </form>
      </div>

      <h1 class="display-5 fw-bold">Results</h1>
      <div class="col-lg-6 mx-auto">
        {loading ? <Spinner /> : ''}
        {!loading && rows.length > 0 ? <ResultTable {...{rows, minimalScore}} /> : ''}
      </div>
    </div>
  );
}

const domContainer = document.querySelector('#app');
const root = ReactDOM.createRoot(domContainer);
root.render(e(App));
