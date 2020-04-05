import React from 'react';
import { StyleSheet, View, Dimensions } from 'react-native';
import { Notifications, AppLoading } from 'expo';
import { Ionicons } from '@expo/vector-icons';
import * as Permissions from 'expo-permissions';
import * as Location from 'expo-location';
import * as Font from 'expo-font';
import MapView, { Marker, Callout, CalloutSubview } from 'react-native-maps';
import { Container, Header, Content, Card, CardItem, Text, Icon, Right, List, ListItem, Button, Switch, Separator, Title, Form, Item, Input, Left, Label, Body, Footer, FooterTab, Spinner, H1, H2, H3 } from 'native-base';
import HelpRequestListComponent from "../../components/help-requests/list";
import HelpRequestsServiceContext from '../../contexts/helpRequestsService';
import { Audio } from 'expo-av';

const permissions : Permissions.PermissionType[] = [
    Permissions.LOCATION,
];

async function checkPermissions() {
    for(let i = 0; i < permissions.length; ++i) {
        const { status } = await Permissions.askAsync(permissions[i]);
        if (status !== 'granted') {
            return false;
        }
    }
    return true;
}

export default class Main extends React.Component {
    static contextType = HelpRequestsServiceContext;

    initialRegion = {
        latitude: 52.2297,
        longitude: 21.0122,
        latitudeDelta: 0.1,
        longitudeDelta: 0.1,
    }

    locationCallback: any = null;
    map: MapView | null = null;

    constructor(props) {
        super(props);
        this.state ={
            hasPermissions: false,
            loaded: false,
            location: null,
            showMap: false,
            entries: []
        };
        this.fetchHelpRequests = this.fetchHelpRequests.bind(this);
    }

    componentDidMount = async () => {
        await Audio.requestPermissionsAsync();
        const hasPermissions = await checkPermissions();
        await Font.loadAsync({
            Roboto: require('native-base/Fonts/Roboto.ttf'),
            Roboto_medium: require('native-base/Fonts/Roboto_medium.ttf'),
            ...Ionicons.font,
        });

        Location.getCurrentPositionAsync();
        this.locationCallback = await Location.watchPositionAsync({}, this.onLocationUpdate);
        this.setState({
            loaded: true,
            hasPermissions
        });
        this.fetchHelpRequests();
        this.interval = setInterval(this.fetchHelpRequests, 5000);
    }

    componentWillUnmount = () => {
        if (this.locationCallback)
            this.locationCallback.remove();

        if (this.interval ) {
            clearInterval(this.interval);
        }
    }

    fetchHelpRequests () {
        this.context.getHelpRequests().then(
            (requests: HelpRequest[]) => {
                this.setState({
                    entries: requests
                });
            }
        ).catch(console.error);
    }

    onLocationUpdate = (location: any) => {
        if(!location.coords || !location.coords.latitude) {
            return;
        }
        if(!this.state.location) {
            // first location update, move map
            if(this.map) {
                this.map.animateCamera({
                    center: {
                        latitude: location.coords.latitude,
                        longitude: location.coords.longitude,
                    },
                    zoom: 12,
                    altitude: 2000
                })
            } else {
                this.initialRegion.latitude = location.coords.latitude;
                this.initialRegion.longitude = location.coords.longitude;
            }
        }
        this.setState({
            location: {
                latitude: location.coords.latitude,
                longitude: location.coords.longitude
            }
        });
    }

    onRegionChange = (region) => {

    }

    renderMap = () => {
        let selfMarker = null;
        if(this.state.location) {
            selfMarker = <Marker pinColor='blue' coordinate={this.state.location}>
                <Callout>
                    <Text>Your location</Text>
                </Callout>
            </Marker>;
        }
        return  <Content><MapView ref={map => { this.map = map }} style={styles.mapStyle} initialRegion={this.initialRegion} onRegionChange={this.onRegionChange}>
            {selfMarker}
            {this.state.entries.map((entry) => {
               return <Marker coordinate={{latitude: entry.address.latitude, longitude: entry.address.longitude}} key={entry.id}>
                    <Callout onPress={
                        () => {
                            this.props.navigation.navigate("HelpSummary", {requestID: entry.id});
                        }
                    }>
                        <Text>{entry.full_name}</Text>
                        <Text>{entry.address.address}</Text>
                    </Callout>
                </Marker> 
            })}
        </MapView></Content>
    }

    render = () => {
        if(!this.state.loaded) {
            return <AppLoading/>;
        }
        return <Container>
            { this.state.showMap ? this.renderMap() : <HelpRequestListComponent requests={this.state.entries} navigation={this.props.navigation}/> }
            <Footer>
                <FooterTab>
                    <Button active={!this.state.showMap} onPress={() => { this.setState({showMap: false})}}>
                        <Text>
                            List
                        </Text>
                    </Button>
                </FooterTab>
                <FooterTab>
                    <Button active={this.state.showMap} onPress={() => { this.setState({showMap: true})}} >
                        <Text>
                            Map
                        </Text>
                    </Button>
                </FooterTab>
            </Footer>
        </Container>
    };
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
    },
    mapStyle: {
        width: Dimensions.get('window').width,
        height: Dimensions.get('window').height,
    },
});