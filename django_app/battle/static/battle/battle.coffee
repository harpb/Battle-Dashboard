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
        password: 'greatsolution'
        isAuthenticated: false
    }
    $scope.login = ->
        console.info('$scope.login')
        Auth.setCredentials(
            $scope.authentication_credentials.username,
            $scope.authentication_credentials.password
        )
        $scope.authentication_credentials.isAuthenticated = true
        getBattles()
        getPlayers()
#        $scope.newPlayerFormToggle()

    # API Endpoints
    playerApi = Restangular.all("player/")
    battleApi = Restangular.all("battle/")

    ########################################################
    # Player
    ########################################################
    $scope.nicknameFilter = ''
    $scope.filterPlayersForm = new AngularForm()
    $scope.filterPlayers = ($event, text = '')->
        $scope.nicknameFilter = text
        console.info('filterPlayers', $event, $scope.nicknameFilter, text)
        getPlayers()
        $event.preventDefault()

    getPlayers = ->
        $scope.filterPlayersForm.submitting = true
        data = {}
        if $scope.nicknameFilter.length > 0
            data.nickname__contains = $scope.nicknameFilter
        console.info('data', $scope.nicknameFilter, data)

        $scope.playerList = playerApi.getList(data).then((response)->
            $scope.filterPlayersForm.submitting = false
            $scope.players = response['objects']
#            console.info('players', $scope.players, $scope.playerList)
        )

    $scope.newPlayerForm = new AngularForm('.new.player.modal')
    $scope.newPlayerForm.addField('nickname', 'Nickname')
    $scope.newPlayerForm.addField('first_name', 'First Name')
    $scope.newPlayerForm.addField('last_name', 'Last Name')

    $scope.savePlayer = ($event) ->
        $event.preventDefault()
        $scope.newPlayerForm.submit(playerApi, $scope.players)

    $scope.editPlayer = (player)->
        player.editing = true

    $scope.updatePlayer = (player)->
        player.editing = false

    # Battles
    exampleDateTime = '2013-12-10 6:10:00'
    $scope.filterBattlesForm = new AngularForm()
    $scope.filterBattlesForm.addField('from', 'Start', placeholder = exampleDateTime)
    $scope.filterBattlesForm.addField('to', 'End', laceholder = exampleDateTime)
    $scope.filterBattles = ($event, start = '', end = '')->
        console.info('filterPlayers', $event, start, end, $scope.filterBattlesForm.fields)
        getBattles()
        $event.preventDefault()

    getBattles = ->
        $scope.filterBattlesForm.submitting = true
        data = {}
        if $scope.filterBattlesForm.fields.from.value and \
                $scope.filterBattlesForm.fields.from.value.length > 0
            data.start__gte = $scope.filterBattlesForm.fields.from.value
        if $scope.filterBattlesForm.fields.to.value and\
                $scope.filterBattlesForm.fields.to.value.length > 0
            data.end__lte = $scope.filterBattlesForm.fields.to.value
        console.info('data', $scope.nicknameFilter, data)
        $scope.battleList = battleApi.getList(data).then((response)->
            $scope.filterBattlesForm.valid = true
            $scope.filterBattlesForm.submitting = false
            $scope.battles = response['objects']
        ,(response)->
            $scope.filterBattlesForm.valid = false
            $scope.filterBattlesForm.submitting = false
            console.info('response.error', response)
            $scope.filterBattlesForm.errors = response.data.error
        )
    $scope.newBattleForm = new AngularForm('.new.battle.modal')
    $scope.newBattleForm.addField('attacker', 'Attacker')
    $scope.newBattleForm.addField('defender', 'Defender')
    $scope.newBattleForm.addField('winner', 'Winner')
    $scope.newBattleForm.addField('start', 'Start', placeholder = exampleDateTime)
    $scope.newBattleForm.addField('end', 'End',
        placeholder = exampleDateTime, defaultValue = exampleDateTime)
    $scope.battlePlayerFields = [
        $scope.newBattleForm.fields.attacker
        $scope.newBattleForm.fields.defender
    ]
    $scope.battleDatetimeFields = [
        $scope.newBattleForm.fields.start
        $scope.newBattleForm.fields.end
    ]
    $scope.saveBattle = ($event) ->
        $event.preventDefault()
        $scope.newBattleForm.submit(battleApi, $scope.battles)

    ########################################################
    # Start the app
    ########################################################
    $scope.login()

########################################################
# Battle App
########################################################
BattleApp = angular.module('BattleApp', ['restangular']);
window.BattleApp = BattleApp
BattleApp.config((RestangularProvider)->
    RestangularProvider.setBaseUrl('/api/v1/')
)
BattleApp.config(($interpolateProvider)->
    $interpolateProvider.startSymbol('<<')
    $interpolateProvider.endSymbol('>>')
)
BattleApp.controller('BattleController', BattleController)