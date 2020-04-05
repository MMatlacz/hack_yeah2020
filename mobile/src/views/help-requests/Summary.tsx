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

export default class HelpRequestSummary extends React.Component<HelpRequestSummaryProps> {
    static contextType = HelpRequestsServiceContext;

    constructor(props: HelpRequestSummaryProps) {
        super(props);
        this.state = {
            isLoading: true,
            requestID: this.props.route.params.requestID,
            helpRequest: null
        }
        this.componentDidMount = this.componentDidMount.bind(this);
    }

    componentDidMount() {
        this.context.getHelpRequest(this.state.requestID).then((helpRequest) => {
            this.setState({isLoading: false, helpRequest})
        });
    }

    render() {
        if(this.state.isLoading) {
            return <AppLoading/>;
        }

        console.log(this.state.helpRequest.phone_number)

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
                        <Icon name={"old-phone"} type={"Entypo"}/><H3>Kontakt </H3>
                        <Text> {this.state.helpRequest.phone_number} </Text>
                    </View>
                    <HelpRequestProducts helpRequest={this.state.helpRequest} checkBox={true} style={styles.contentItem}/>
                </Container>
            </Content>
            <Footer>
                <FooterTab>
                    <Button active={true} onPress={() => {}}>
                        <Text>Dowieziono!</Text>
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
