import React, { Component } from 'react';
import axios from 'axios'
import './App.css';

class App extends Component {

  state = {
    selectedFile: null,
    results: [],
    gender: 'X',
    minMoney: 0,
    maxMoney: 100000
  }

  handleGenderChange = event => {
    this.setState({
      gender: event.target.value
    })
  }

  handleMinMoneyChange = event => {
    this.setState({
      minMoney: event.target.value
    })
  }

  handleMaxMoneyChange = event => {
    this.setState({
      maxMoney: event.target.value
    })
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

    let url = 'http://localhost:5000/query/'.concat(this.state.gender)
    url = url.concat('/')
    url = url.concat(this.state.minMoney)
    url = url.concat('/')
    url = url.concat(this.state.maxMoney)

    axios.post(url, fd, config)
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
        <img class="header" src="heading.png" alt="Fasion Bot Header"></img>
        <div class="sidebar">
          <img class="subheader" src="image.jpeg" alt="Fasion Bot Header"></img>
          <label class="file_container">
            <input type="file" class="inputfile" onChange={this.fileSelectedHandler}/>
          </label>
          <img class="subheader" src="gender.jpeg" alt="Fasion Bot Header"></img>
          <select value={this.state.gender} onChange={this.handleGenderChange}>
            <option value="M">Male</option>
            <option value="F">Female</option>
            <option value="X">Either</option>
          </select>
          <img class="subheader" src="price.jpeg" alt="Fasion Bot Header"></img>
          <input type="number" placeholder="Min Budget" onChange={this.handleMinMoneyChange}/>
          <input class="smt" type="number" placeholder="Max Budget" onChange={this.handleMaxMoneyChange}/>
          <button onClick={this.fileUploadHandler}>Search</button>
        </div>
        <div class="images">
          {this.state.results.map(item =>
            (<div>
              <a href={item.url}>
                <img src={item.images} alt="pic" class="img-thumbnail"/>
              </a>
              <p>
                {"$" + item.price + " "}
                <p class="caps">{item.product_brand}</p>
                <p class="low">{item.product_name}</p>
              </p>
            </div>),
          )}
        </div>
      </div>
    );
  }
}

export default App;
