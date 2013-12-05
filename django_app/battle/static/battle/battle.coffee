########################################################
# Battle Controller
########################################################
BattleController = ($scope, Restangular, Auth) ->

#    console.info('Auth', Auth, Auth.setCredentials('harp', 'great'))

    ########################################################
    # Basic Auth
    ########################################################
    $scope.authentication_credentials = {
        username: 'harp'
        password: 'great'
        isAuthenticated: false
    }
    $scope.login = ->
        Auth.setCredentials(
            $scope.authentication_credentials.username,
            $scope.authentication_credentials.password
        )
        $scope.authentication_credentials.isAuthenticated = true
        getBattles()
        getPlayers()

    # API Endpoints
    playerApi = Restangular.all("player/")
    battleApi = Restangular.all("battle/")

    # Players
    getPlayers = ->
        $scope.playerList = playerApi.getList().then((response)->
            $scope.players = response['objects']
            console.info('players', $scope.players, $scope.playerList)
        )

    $scope.playerPayload =
        first_name: ''
        last_name: ''
        nickname: ''

    $scope.savePlayer = () ->
        $scope.playerPayload.loading = true
        playerApi.post($scope.playerPayload).then((response)->
            $scope.playerPayload.loading = false
            $scope.players.push(response)
            $scope.resetNewPlayerForm()
        )

    $scope.editPlayer = (player)->
        player.editing = true

    $scope.updatePlayer = (player)->
        player.editing = false
#        $scope.playerList.put(player)
#        playerApi.put(player)

    $scope.newPlayerForm = ->
        $('.new.player.modal')
        .modal('setting',
                'transition': 'horizontal flip'
                onApprove: ->
                    return false
            )
        .modal('toggle')

    $scope.resetNewPlayerForm = ->
        $scope.playerPayload =
            first_name: ''
            last_name: ''
            nickname: ''
        $scope.newPlayerForm()

    # Battles
    getBattles = ->
        $scope.battleList = battleApi.getList().then((response)->
            $scope.battles = response['objects']
        )

    $scope.newBattleForm = ->
        $('.new.battle.modal')
        .modal('setting',
                'transition': 'horizontal flip'
                onApprove: ->
                    return false
            )
        .modal('toggle')

    $scope.resetNewBattleForm = ->
        $scope.battlePayload =
            attacker: null
            defender: null
            attacker_wins: false
            start: currentDate.toISOString()
            end: currentDate.toISOString()
        $scope.newBattleForm()

    currentDate = new Date()
    $scope.battlePayload =
        attacker: null
        defender: null
        attacker_wins: false
        start: currentDate.toISOString()
        end: currentDate.toISOString()

    $scope.saveBattle = () ->
        $scope.battlePayload.loading = true
        if $scope.battlePayload.attacker_wins
            $scope.battlePayload.winner = $scope.battlePayload.attacker
        else
            $scope.battlePayload.winner = $scope.battlePayload.defender

        battleApi.post($scope.battlePayload).then((response)->
            $scope.battlePayload.loading = false
            $scope.battles.push(response)
            $scope.resetNewBattleForm()
        )

    # Ready
    $scope.login()
#    $scope.savePlayer()

########################################################
# Battle App
########################################################
BattleApp = angular.module('BattleApp', ['restangular']);
window.BattleApp = BattleApp
#window.battleApp = BattleApp
BattleApp.config((RestangularProvider)->
    RestangularProvider.setBaseUrl('/api/v1/')
)
BattleApp.config(($interpolateProvider)->
    $interpolateProvider.startSymbol('<<')
    $interpolateProvider.endSymbol('>>')
)
BattleApp.controller('BattleController', BattleController)