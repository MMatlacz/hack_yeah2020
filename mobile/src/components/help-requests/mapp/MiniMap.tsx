import MapView, {Marker} from "react-native-maps";
import { View } from 'native-base';

import React from "react";
import {Dimensions} from "react-native";

class HelpRequestMiniMap extends React.Component<HelpListItemProps> {
    initialRegion = {
        latitude: 52.2297,
        longitude: 21.0122,
        latitudeDelta: 0.1,
        longitudeDelta: 0.1,
    };
    mapView: MapView;

    constructor(props: HelpListItemProps) {
        super(props);
        this.componentDidMount = this.componentDidMount.bind(this);
    }

    componentDidMount(): void {
        setTimeout(() => {
            this.mapView.animateCamera({
                center: {
                    latitude: this.props.helpRequest.address.latitude,
                    longitude: this.props.helpRequest.address.longitude,
                },
                zoom: 12,
                altitude: 2000,
            }, {duration:1500})
        }, 1000);
    }

    render() {
        return (
            <View>
                <MapView ref={(mapView) => { this.mapView = mapView }} style={styles.mapStyle} initialRegion={this.initialRegion}>
                    <Marker
                        coordinate={this.props.helpRequest.address}
                        description={`Adres dostawy: ${this.props.helpRequest.address.address}`}
                        title={`Zakupy dla: ${this.props.helpRequest.full_name}`}
                    />
                </MapView>
            </View>
        );
    }
}

const styles = {
    mapStyle: {
        width: Dimensions.get('window').width,
        height: Dimensions.get('window').height / 4,
    },
}

type HelpListItemProps = {
    helpRequest: HelpRequest
}

export default HelpRequestMiniMap;
