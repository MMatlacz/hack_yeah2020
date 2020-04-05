import {Body, Container, Footer, Form, FooterTab, Header, Text, Title, Button, Content, Item, Input, Label} from "native-base";
import React from "react";


export default class LogIn extends React.Component {
    state = {
        registration: false,
        error: null
    }

    pressed = async () => {
        try {
            if(this.state.registration) {
                await this.props.userSerivice.registerUser({
                    first_name: "name",
                    last_name: "surname",
                    email: this.state.email,
                    username: "user",
                    password: this.state.password
                });
            } else {
                await this.props.userSerivice.logIn(this.state.email, this.state.password);
            }
        } catch(e) {
            this.setState({error: e});
        }
    }

    render = () => {
        return (
            <Container>
                <Content>
                    <Form>                        
                        <Item floatingLabel>
                            <Label>Email</Label>
                            <Input
                                autoCapitalize="none"
                                placeholder="Email"
                                autoCompleteType="email"
                                keyboardType="email-address"
                                textContentType="emailAddress"
                                onChangeText={email => this.setState({ email })}
                            />
                        </Item>
                        <Item floatingLabel last>
                            <Label>Password</Label>
                            <Input
                                secureTextEntry={true}
                                placeholder="Password"
                                autoCompleteType="password"
                                onChangeText={password => this.setState({ password })}
                            />
                        </Item>
                    </Form>
                    <Button
                        onPress={this.pressed}
                        style={{marginTop: 20}}
                    >
                        <Text> {this.state.registration ? 'Register' : 'Login' } </Text>
                    </Button>
                    { this.state.error ? <Text>{this.state.error}</Text> : <></>}
                </Content>
                <Footer>
                    <FooterTab>
                        <Button active={!this.state.registration} onPress={() => { this.setState({registration: false}) }}>
                            <Text>Login</Text>
                        </Button>
                    </FooterTab>
                    <FooterTab>
                        <Button active={this.state.registration} onPress={() => { this.setState({registration: true}) }} >
                            <Text>Register</Text>
                        </Button>
                    </FooterTab>
                </Footer>
            </Container>
        )
    };
}