import React, { Component } from 'react';
import axios from 'axios'
import './App.css';

class App extends Component {

  state = {
    selectedFile: null,
    results: []
  }

  fileSelectedHandler = event => {
    this.setState({
      selectedFile: event.target.files[0]
    })
  }

  fileUploadHandler = () => {
    const fd = new FormData();
    fd.append('file', this.state.selectedFile, this.state.selectedFile.name);

    var config = {
      headers: {'Access-Control-Allow-Origin': '*'}
    };

    axios.post('http://localhost:5000/query/M', fd, config)
      .then(res => {
        console.log(res)
        this.setState({
          results: res.data.results
        })
      });
  }

  render() {
    return (
      <div className="App">
        <input type="file" onChange={this.fileSelectedHandler}/>
        <button onClick={this.fileUploadHandler}>Upload</button>
      {this.state.results.map(item =>
        (<div>
          <a href={item.url}>
            <img src={item.images} alt="pic"/>
          </a>
          {item.price}
          {item.product_brand}
          {item.product_name}
        </div>),
      )}
      </div>
    );
  }
}

export default App;
