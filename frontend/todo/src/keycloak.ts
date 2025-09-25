import Keycloak from 'keycloak-js'

const keycloakConfig = {
    url: 'http://localhost:8000',
    realm: 'todo',
    clientId: 'todo-react',
};

const keycloak = new Keycloak(keycloakConfig);

export default keycloak;