import React from "react";
import {
    Container,
    Header,
    Content,
    Text,
    Icon,
    Button,
    Title,
    Body,
    Footer,
    FooterTab,
    H3,
    Left,
    Right
} from 'native-base';
import HelpRequestsService from "../../data/HelpRequests";
import { AppLoading } from "expo";
import HelpRequestsServiceContext from "../../contexts/helpRequestsService";
import MapView from "react-native-maps";
import HelpRequestProducts from "../../components/help-requests/common/HelpRequestProducts";
import HelpRequestMiniMap from "../../components/help-requests/mapp/MiniMap";
import {View} from "react-native";
import { Audio } from 'expo-av';

export default class HelpRequestSummary extends React.Component<HelpRequestSummaryProps> {
    static contextType = HelpRequestsServiceContext;
    soundObject = new Audio.Sound();

    constructor(props: HelpRequestSummaryProps) {
        super(props);
        this.state = {
            isLoading: true,
            requestID: this.props.route.params.requestID,
            helpRequest: null,
            playing: false
        }
        this.componentDidMount = this.componentDidMount.bind(this);
    }

    componentDidMount() {
        this.context.getHelpRequest(this.state.requestID).then((helpRequest) => {
            this.setState({isLoading: false, helpRequest})
        });
    }

    async componentWillUnmount() {
        if(this.state.playing) {
            await this.soundObject.stopAsync();
            this.setState({
                playing: false
            });
            return;
        }        
    }

    takeHelpRequest = async () => {
        await this.context.assignForHelp(this.state.requestID);
    }

    playAudio = async () => {
        if(this.state.playing) {
            this.soundObject.stopAsync();
            this.setState({
                playing: false
            });
            return;
        }
        try {
          console.log(this.state.helpRequest.recording_url);
          this.setState({
              playing: true
          });
          await this.soundObject.loadAsync({ uri: this.state.helpRequest.recording_url });
          await this.soundObject.playAsync();          
        } catch (error) {
          console.log(error);
        }        
    }

    render() {
        if(this.state.isLoading) {
            return <AppLoading/>;
        }

        let recording = null;
        if(this.state.helpRequest.recording_url) {
            recording = <View style={styles.contentItem}>
                <Button onPress={this.playAudio}>
                    <Text>{ !this.state.playing ? 'Odtwórz nagranie' : 'Zatrzymaj nagranie' }</Text>
                </Button>
            </View>;
        }
        console.log(this.state.helpRequest.recording_url)

        return <Container>
            <Header>
                <Body>
                    <Title>Pomoc dla: {this.state.helpRequest.full_name}</Title>
                </Body>
            </Header>
            <Content>
                <Container>
                    <HelpRequestMiniMap helpRequest={this.state.helpRequest} style={styles.contentItem}/>
                    <View style={styles.contentItem}>
                        <H3>Adres</H3>
                        <Text>{this.state.helpRequest.address.address}</Text>
                    </View>

                    <View style={styles.contentItem}>
                        <H3><Icon name={"old-phone"} type={"Entypo"}/>  Kontakt:</H3>
                        <Text> {this.state.helpRequest.phone_number} </Text>
                    </View>

                    {recording}

                    <HelpRequestProducts helpRequest={this.state.helpRequest} checkBox={true} style={styles.contentItem}/>
                </Container>
            </Content>
            <Footer>
                <FooterTab>
                    <Button active={true} onPress={this.state.takeHelpRequest}>
                        <Text>Zrealizowano!</Text>
                    </Button>
                </FooterTab>
            </Footer>
        </Container>
    }
}

const styles = {
    contentItem: {
        marginTop: 20,
        marginBottom: 20,
    }
}

type HelpRequestSummaryProps = {
    helpRequestService: HelpRequestsService
}
