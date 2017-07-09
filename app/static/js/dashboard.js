


var Navbar = React.createClass({

  render: function(){
    // console.log(this.state)
    return(
        <nav className="navbar navbar-default">
          <div className="container">
            <div className="navbar-header">
              <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                <span className="sr-only">Toggle navigation</span>
                <span className="icon-bar"></span>
                <span className="icon-bar"></span>
                <span className="icon-bar"></span>
              </button>
              <a className="navbar-brand" href="#">Street Witness</a>
            </div>

            <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
              <ul className="nav navbar-nav">
                <li className="active"><a href="#">Dashboard <span className="sr-only">(current)</span></a></li>
                <li><a href="#">Map</a></li>
              </ul>
              <form className="navbar-form navbar-left" role="search">
                <div className="form-group">
                  <input type="text" className="form-control" placeholder="Search" />
                </div>
                <button type="submit" className="btn btn-default">Submit</button>
              </form>
              <ul className="nav navbar-nav navbar-right">
                <li><a href="#">Logout (TODO)</a></li>
              </ul>
            </div>
          </div>
        </nav>
    )
  }

})


var Incident = React.createClass({

  render: function(){
  console.log('this.props')
  console.log(this.props)
    return(
      <div className="col-md-4 col-sm-6">
        <div className="panel panel-success">
          <div className="panel-heading">
            <h3 className="panel-title">{this.props.incident.title}</h3>
          </div>
          <div className="panel-body">
            <h4>{this.props.incident.description}</h4>
          </div>
        </div>
      </div>
    )
  }

})


var Body = React.createClass({

  render: function(){
    console.log(this.props)

    var pendingIncidentsList = this.props.pendingIncidents.incidents.map(function(incident){
      return <Incident incident={incident} key={incident.timestamp} />
    })

    var activeIncidentsList = this.props.activeIncidents.incidents.map(function(incident){
      return <Incident incident={incident} key={incident.timestamp} />
    })

    var archivedIncidentsList = this.props.archivedIncidents.incidents.map(function(incident){
      return <Incident incident={incident} key={incident.timestamp} />
    })

    return(
      <div className="container">
        <ul className="nav nav-tabs">
          <li className="active"><a href="#pending" data-toggle="tab">Pending <span className="badge">{this.props.pendingIncidents.count}</span></a></li>
          <li><a href="#active" data-toggle="tab">Active <span className="badge">{this.props.activeIncidents.count}</span></a></li>
          <li><a href="#archived" data-toggle="tab">Archived <span className="badge">{this.props.archivedIncidents.count}</span></a></li>
        </ul>
        <div id="tabContent" className="tab-content">
          <div className="tab-pane fade active in" id="pending">
            <div className="row">
              <h3 className="text-center text-success">Pending Incidents</h3>
              {pendingIncidentsList}
            </div>
          </div>
          <div className="tab-pane fade" id="active">
            <div className="row">
              <h3 className="text-center text-success">Active Incidents</h3>
              {activeIncidentsList}
            </div>
          </div>
          <div className="tab-pane fade" id="archived">
            <div className="row">
              <h3 className="text-center text-success">Archived Incidents</h3>
              {archivedIncidentsList}
            </div>
          </div>
        </div>
      </div>
    )
  }

})



var Login = React.createClass({

  render: function(){

    if(this.props.error){
      var alert = <div className="alert alert-warning">
                      {this.props.error}
                  </div>
    }

    return(
      <div className="modal show">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h4 className="modal-title text-center">Please Login</h4>
            </div>
              <form action="" className="form-horizontal" onSubmit={this.props.handleSubmit}>
            <div className="modal-body">
                <div className="form-group">
                  <label htmlFor="username" className="col-sm-2 control-label">Username</label>
                  <div className="col-sm-10">
                    <input type="text" className="form-control" id="username" placeholder="Username" />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="password" className="col-sm-2 control-label">Password</label>
                  <div className="col-sm-10">
                    <input type="password" className="form-control" id="password" placeholder="Password" />
                  </div>
                </div>
                {alert}
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-default" data-dismiss="modal">Clear</button>
              <button type="submit" className="btn btn-success">Submit</button>
            </div>
               </form>
          </div>
        </div>
      </div>
    )
  }

})



var App = React.createClass({
  getInitialState: function(){
    return(
      {
        "loggedIn": false
      }
    )
  },


  componentDidMount: function(){
    if(localStorage.authToken){
      console.log('token exist')

    var incidentsUrl = 'http://127.0.0.1:5000/api/incidents/'
    var pendingIncidentsUrl = incidentsUrl + '?status=pending'
    var activeIncidentsUrl = incidentsUrl + '?status=active'
    var archivedIncidentsUrl = incidentsUrl + '?status=archived'

    fetch(pendingIncidentsUrl, {
      method: 'GET',
      headers: {'Content-Type': 'application/json',
                 'Authorization': 'Bearer ' + localStorage.authToken},
    }).then(function(response){
        console.log(response)
        return response.json()
        }).then(function(result){
            if(result.status === 'Fail'){
              console.log('error')
              console.log(result)
            }

            else{
              console.log('result')
              console.log(result)

              this.setState({
                "loggedIn": true,
                "pendingIncidents": result
              })
            }
        }.bind(this))

    fetch(activeIncidentsUrl, {
      method: 'GET',
      headers: {'Content-Type': 'application/json',
                 'Authorization': 'Bearer ' + localStorage.authToken},
    }).then(function(response){
        console.log(response)
        return response.json()
        }).then(function(result){
            if(result.status === 'Fail'){
              console.log('error')
              console.log(result)
            }

            else{
              console.log('result')
              console.log(result)

              this.setState({
                "loggedIn": true,
                "activeIncidents": result
              })
            }
        }.bind(this))


    fetch(archivedIncidentsUrl, {
      method: 'GET',
      headers: {'Content-Type': 'application/json',
                 'Authorization': 'Bearer ' + localStorage.authToken},
    }).then(function(response){
        console.log(response)
        return response.json()
        }).then(function(result){
            if(result.status === 'Fail'){
              console.log('error')
              console.log(result)
            }

            else{
              console.log('result')
              console.log(result)

              this.setState({
                "loggedIn": true,
                "archivedIncidents": result
              })
            }
        }.bind(this))



    }



    else{
      console.log('token does not exist')
    }
  },


  handleSubmit: function(e){

    e.preventDefault()

    var loginUrl = 'http://127.0.0.1:5000/auth/login'
    var body = JSON.stringify({username: e.target.username.value,
                               password: e.target.password.value
    })

    fetch(loginUrl, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: body
    }).then(function(response){
        console.log(response)
        return response.json()
        }).then(function(result){
            if(result.status === 'Success'){
              console.log('result')
              console.log(result)

              localStorage.authToken = result.auth_token

              this.setState({
                "loggedIn": true
              })
            }

            else{
              console.log('error')
              console.log(result)

              this.setState({
                "error": result.message
              })
            }

        }.bind(this))
  },


// fetch(loginUrl, {
//   method: 'POST',
//   headers: {'Content-Type': 'application/json',
//              Authorization: "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTkwMDc2ODAsImlhdCI6MTQ5ODkyMTI4MCwic3ViIjoxMiwicm9sZSI6IlVzZXIifQ.QDmaS_BeW3OpAYw8UluPVfeBxyiKEM6fP5TjhAT71n4"}
// }).then(function(response){
//     console.log(response)
//     return response.json()
//     }).then(function(result){
//         if(result.status == 200){
//           console.log('result')
//           console.log(result)
//         }
//         else{
//           console.log('error')
//           console.log(result)
//         }
//     })



  render: function(){

    console.log('this.state')
    console.log(this.state)

    if(this.state.loggedIn && this.state.archivedIncidents){
      return(
        <div className="row">
          <Navbar />
          <Body pendingIncidents={this.state.pendingIncidents}
                activeIncidents={this.state.activeIncidents}
                archivedIncidents={this.state.archivedIncidents} />
        </div>
      )
    }

    return(
      <div className="row">
        <div className="col-sm-4 col-sm-offset-4">
          <i className="fa fa-spinner fa-pulse fa-3x fa-fw"></i>
          <span className="sr-only">Loading...</span>
        </div>
      </div>
      // <Login handleSubmit={this.handleSubmit} error={this.state.error}/>
    )


  }
})


ReactDOM.render(
  <App />,
  document.getElementById('app')
)

// redesign w/ single component - App? 
// Then state (map) will be updated more smoothly?



  // * check for logged in user properly;
  // * loading gif on each tab;
