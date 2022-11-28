'use strict';

const e = React.createElement;
const { useState } = React;
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  headers: {
    'ContentType': 'application/json',
  },
});

function SearchButton({ text }) {
  const [enabled, setEnabled] = useState(true);
  const click = async () => {
    if (enabled) {
      setEnabled(false);
      try {
        const response = await api.post('/search', {text});
      } catch(e) {
      }
      setEnabled(true);
    }
  }

  return (
    <button onClick={click} type="button" class="btn btn-primary btn-lg px-4 gap-3 m-2" enabled={enabled}>Search</button>
  )
}

function CancelButton({ handleClick }) {
  return (
    <button onClick={handleClick} type="button" class="btn btn-outline-secondary btn-lg px-4 m-2">Clear</button>
  )
}

function App() {
  const [text, setText] = useState('');

  const handleChange = (e) => {
    setText(e.target.value)
  };

  const handleClick = () => {
    setText('');
  };

  return (
    <div class="px-4 py-5 my-5 text-center">
      <h1 class="display-5 fw-bold">Check text uniqueness</h1>
      <div class="col-lg-6 mx-auto">
        <form>
          <div class="form-group">
            <textarea onChange={handleChange} placeholder="Enter text..." class="form-control" id="search-text" rows="5" value={text}></textarea>
          </div>
          <div class="form-group">
            <div class="d-grid gap-2 d-sm-flex justify-content-sm-center">
              <SearchButton text={text}/>
              <CancelButton handleClick={handleClick}/>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

const domContainer = document.querySelector('#app');
const root = ReactDOM.createRoot(domContainer);
root.render(e(App));
