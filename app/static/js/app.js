
var GoogleMap = React.createClass({
  getDefaultProps: function(){
    return{
      initialZoom: 13,
      centerLat: 49.84104,
      centerLng: 24.03164
    }
  },

  componentWillReceiveProps: function(nextProps){
    var mapOptions = {center: {lat: this.props.centerLat,
                               lng: this.props.centerLng},
                      zoom: this.props.initialZoom,
                      mapTypeControl: false
    },

    map = new google.maps.Map(document.getElementById('map'), mapOptions)

    var btnContainer = document.createElement('div')
    btnContainer.id = 'btn-container-div'

    var btn = $('<button class="btn btn-info" id="add-incident-btn" \
                         title="Додати інцидент" data-toggle="modal" \
                         data-target="#add-incident-modal">Додати інцидент</button>')

    btnContainer.appendChild(btn[0])

    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(btnContainer);

    $.getJSON("static/js/map-styles.json", function(data){
        map.setOptions({styles: data})
    })

    // console.log(nextProps.incidents)

    nextProps.incidents.forEach(function(item){
      // console.log(item)
      var marker = new google.maps.Marker({
        position: item.location,
        // position: JSON.parse(item.location),
        map: map,
        title: item.title
      })


      // var content = '<h3 class="text-success">' + item.title + '</h3>'
      // var content = <div>
      // <h4>Title</h4>
      // <p>descr</p>
      // <span class="label label-default">{incident.tag}</span>
      // <p></p>
      // </div>

      // var content = '<div><h4 class="text-info">' + item.title + '</h4>' +
      //               '<pre>' + item.description + '</pre>' +
      //               '<span class="label label-info">' + item.tag + '</span>' +
      //               '<p>' + new Date(item.date.$date).toLocaleString() + '</p></div>'

      var content = '<div id="content"><h4 class="text-info">' + item.title + '</h4>' +
                    '<p>' + new Date(item.timestamp) + '</p>' +
                    '<pre>' + item.description + '</pre>' +
                    '<span class="label label-info">' + item.tag + '</span></div>'

      var infowindow = new google.maps.InfoWindow()

      google.maps.event.addListener(marker, 'click', (function(marker,content,infowindow){
              return function(){
                 infowindow.setContent(content)
                 infowindow.open(map,marker)
              }
          })(marker,content,infowindow))

      return marker
    })

},



//   componentDidMount: function(){
//     var mapOptions = {center: {lat: this.props.centerLat,
//                                lng: this.props.centerLng},
//                       zoom: this.props.initialZoom,
//                       mapTypeControl: false
//     },

//     map = new google.maps.Map(document.getElementById('map'), mapOptions)

//     var btnContainer = document.createElement('div')
//     btnContainer.id = 'btn-container-div'

//     var btn = $('<button class="btn btn-info" id="add-incident-btn" \
//                          title="Додати інцидент" data-toggle="modal" \
//                          data-target="#add-incident-modal">Додати інцидент</button>')

//     btnContainer.appendChild(btn[0])

//     map.controls[google.maps.ControlPosition.TOP_RIGHT].push(btnContainer);

//     $.getJSON("static/js/map-styles.json", function(data){
//         map.setOptions({styles: data})
//     })

// },




  render: function(){
    return(
      <div id="map"></div>
    )
  }

})


var FormModal = React.createClass({
  getInitialState: function(){
    return{
      title: '',
      description: '',
      location: '',
      locationText: '',
      tag: ''
    }
  },

  useCurrentLocation: function(){
    var currentLocation

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position){
          currentLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          }
          console.log(currentLocation)
          this.setState({
            location: currentLocation,
            locationText: 'Поточні координати'
          })
        }.bind(this));
    }

    // var geocoder = new google.maps.Geocoder;

    // console.log(currentLocation)

    // geocoder.geocode({'location': currentLocation}, function(results, status) {
    //   if (status === 'OK') {
    //     console.log(results)
    //   }

    //   else {
    //     window.alert('Geocoder failed due to: ' + status);
    //   }
    // });

  },

  handleChange: function(event){
    var target = event.target
    var name = target.name
    var value = target.value
    // console.log(name, value)
    this.setState({
      [name]: value
    })

  },

  handleSubmit: function(event){
    event.preventDefault()

    var url = 'http://127.0.0.1:5000/api/incidents/'

    fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(this.state)
    }).then(function(response){
      console.log(response.json())
    })

    this.props.fetch()
    this.clearState()
    $("#add-incident").trigger('reset')
    $("#add-incident-modal").modal('toggle')
  },

  clearState: function(){
    this.setState({
      title: '',
      description: '',
      location: '',
      locationText: '',
      tag: ''
    })
  },


  render: function(){
    // console.log(this.state)
    return(
      <div className="modal" id="add-incident-modal">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <button type="button"
                      className="close"
                      data-dismiss="modal"
                      aria-hidden="true">&times;
              </button>
              <h4 className="modal-title">Додати Інцидент</h4>
            </div>

            <form action="" className="form-horizontal" id="add-incident" onSubmit={this.handleSubmit}>
            <div className="modal-body">
                <div className="form-group">
                  <label className="col-md-2">Інцидент:</label>
                  <div className="col-md-10">
                    <input type="text"
                           className="form-control"
                           placeholder="ДТП, крадіжка, тощо"
                           name="title"
                           onChange={this.handleChange} />
                  </div>
                </div>

                <div className="form-group">
                  <label className="col-md-2">Опис:</label>
                  <div className="col-md-10">
                    <textarea className="form-control" rows="4"
                              placeholder='Додайте опис'
                              name="description"
                              onChange={this.handleChange}></textarea>
                  </div>
                </div>

                <div className="form-group">
                  <label className="col-md-2">Місце події:</label>
                  <div className="col-md-10">
                      <input type="text"
                             className="form-control"
                             placeholder="Поточне "
                             name="location"
                             value={this.state.locationText}
                             onChange={this.handleChange} />
                      <i className="fa fa-location-arrow fa-lg inline-btn"
                         title="Використати поточне місцезнаходження"
                         onClick={this.useCurrentLocation}></i>
                  </div>
                </div>

                <div className="form-group">
                  <label className="col-md-2">Тег:</label>
                  <div className="col-md-10">
                    <input type="text"
                           className="form-control"
                           placeholder="ДТП, крадіжка, тощо"
                           name="tag"
                           onChange={this.handleChange} />
                  </div>
                </div>

            </div>

            <div className="modal-footer">
              <button type="button" className="btn btn-default" 
                      data-dismiss="modal">Закрити</button>
              <button type="submit" className="btn btn-info">Додати</button>
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
    return{
      incidents: []
    }
  },

  fetchIncidents: function(){
    // var url = 'http://127.0.0.1:5000/api/incidents?status=active'
    var url = 'http://127.0.0.1:5000/api/incidents/?status=active'
    var incidents

    $.ajax({
      url: url,
      dataType: 'json',
      cache: false,
      success: function(data){
        // console.log(data)
        this.setState({
          incidents: data.incidents
        })
      }.bind(this),

      error: function(xhr, status, err) {
        console.error(status, err.toString());
      }
    })
  },

  componentDidMount: function(){
    this.fetchIncidents()
  },

  render: function(){
    // console.log(this.state)
    return(
      <div className="row">
        <GoogleMap incidents={this.state.incidents} />
        <FormModal fetch={this.fetchIncidents} />
      </div>
    )
  }
})


ReactDOM.render(
  <App />,
  document.getElementById('app')
)

// redesign w/ single component - App? 
// Then state (map) will be updated more smoothly?