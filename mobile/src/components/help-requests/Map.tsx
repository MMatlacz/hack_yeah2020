import React from 'react';
import { StyleSheet, View, Dimensions } from 'react-native';
import { Notifications } from 'expo';
import { Ionicons } from '@expo/vector-icons';
import * as Permissions from 'expo-permissions';
import * as Location from 'expo-location';
import * as Font from 'expo-font';
import MapView, { Marker } from 'react-native-maps';
import { Content } from 'native-base';

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

export default class MapView extends React.Component {
    state = {
        hasPermissions: false,
        loaded: false,
        location: null,
    }

    initialRegion = {
        latitude: 52.2297,
        longitude: 21.0122,
        latitudeDelta: 0.1,
        longitudeDelta: 0.1,
    }

    locationCallback: any = null;
    map: MapView | null = null;

    componentDidMount = async () => {
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
    }

    componentWillUnmount = () => {
        if (this.locationCallback) {
            this.locationCallback.remove();
        }
    }

    onLocationUpdate = (location: any) => {
        if (!location.coords || !location.coords.latitude) {
            return;
        }
        if (!this.state.location) {
            // first location update, move map
            if (this.map) {
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

    render = () => {
        return (
            <Content>
                <MapView ref={map => {
                    this.map = map
                }} style={styles.mapStyle} initialRegion={this.initialRegion} onRegionChange={this.onRegionChange}>
                    {this.state.location ?
                        <Marker coordinate={this.state.location}></Marker> :
                        null
                    }
                </MapView>
            </Content>
        );
    }
};

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