from tests import unittest, mock, Redmine, URL
from redmine.resultsets import ResourceSet

responses = {
    'project': {
        'get': {'project': {'name': 'Foo', 'id': 1}},
        'all': {'projects': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'issue': {
        'get': {'issue': {'subject': 'Foo', 'id': 1}},
        'all': {'issues': [{'subject': 'Foo', 'id': 1}, {'subject': 'Bar', 'id': 2}]},
        'filter': {'issues': [{'subject': 'Foo', 'id': 1}, {'subject': 'Bar', 'id': 2}]},
    },
    'time_entry': {
        'get': {'time_entry': {'hours': 2, 'id': 1}},
        'all': {'time_entries': [{'hours': 3, 'id': 1}, {'hours': 4, 'id': 2}]},
        'filter': {'time_entries': [{'hours': 3, 'id': 1}, {'hours': 4, 'id': 2}]},
    },
    'enumeration': {
        'filter': {'time_entry_activities': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'attachment': {
        'get': {'attachment': {'filename': 'foo.jpg', 'id': 1}},
    },
    'wiki_page': {
        'get': {'wiki_page': {'title': 'Foo'}},
        'filter': {'wiki_pages': [{'title': 'Foo'}, {'title': 'Bar'}]},
    },
    'project_membership': {
        'get': {'membership': {'id': 1}},
        'filter': {'memberships': [{'id': 1}, {'id': 2}]},
    },
    'issue_category': {
        'get': {'issue_category': {'id': 1, 'name': 'Foo'}},
        'filter': {'issue_categories': [{'id': 1, 'name': 'Foo'}, {'id': 2, 'name': 'Bar'}]},
    },
    'issue_relation': {
        'get': {'relation': {'id': 1}},
        'filter': {'relations': [{'id': 1}, {'id': 2}]},
    },
    'version': {
        'get': {'version': {'id': 1, 'name': 'Foo'}},
        'filter': {'versions': [{'id': 1, 'name': 'Foo'}, {'id': 2, 'name': 'Bar'}]},
    },
    'user': {
        'get': {'user': {'firstname': 'John', 'id': 1}},
        'all': {'users': [{'firstname': 'John', 'id': 1}, {'firstname': 'Jack', 'id': 2}]},
        'filter': {'users': [{'firstname': 'John', 'id': 1}, {'firstname': 'Jack', 'id': 2}]},
    },
    'group': {
        'get': {'group': {'name': 'Foo', 'id': 1}},
        'all': {'groups': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'role': {
        'get': {'role': {'name': 'Foo', 'id': 1}},
        'all': {'roles': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'news': {
        'all': {'news': [{'title': 'Foo', 'id': 1}, {'title': 'Bar', 'id': 2}]},
        'filter': {'news': [{'title': 'Foo', 'id': 1}, {'title': 'Bar', 'id': 2}]},
    },
    'issue_status': {
        'all': {'issue_statuses': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'tracker': {
        'all': {'trackers': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'query': {
        'all': {'queries': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'custom_field': {
        'all': {'custom_fields': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
}


class TestResources(unittest.TestCase):
    def setUp(self):
        self.url = URL
        self.redmine = Redmine(self.url)
        self.response = mock.Mock(status_code=200)
        patcher = mock.patch('requests.get', return_value=self.response)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_resource_supports_dictionary_like_attr_retrieval(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertEqual(project['id'], 1)
        self.assertEqual(project['name'], 'Foo')

    def test_resource_supports_url_retrieval(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(self.redmine.project.get(1).url, '{}/projects/1'.format(self.url))

    def test_project_version(self):
        self.assertEqual(self.redmine.project.resource_class.version, '1.0')

    def test_project_get(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertEqual(project.id, 1)
        self.assertEqual(project.name, 'Foo')

    def test_project_all(self):
        self.response.json.return_value = responses['project']['all']
        projects = self.redmine.project.all()
        self.assertEqual(projects[0].id, 1)
        self.assertEqual(projects[0].name, 'Foo')
        self.assertEqual(projects[1].id, 2)
        self.assertEqual(projects[1].name, 'Bar')

    def test_project_relations(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertIsInstance(project.wiki_pages, ResourceSet)
        self.assertIsInstance(project.memberships, ResourceSet)
        self.assertIsInstance(project.issue_categories, ResourceSet)
        self.assertIsInstance(project.versions, ResourceSet)
        self.assertIsInstance(project.news, ResourceSet)
        self.assertIsInstance(project.issues, ResourceSet)

    def test_issue_version(self):
        self.assertEqual(self.redmine.issue.resource_class.version, '1.0')

    def test_issue_get(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.assertEqual(issue.id, 1)
        self.assertEqual(issue.subject, 'Foo')

    def test_issue_all(self):
        self.response.json.return_value = responses['issue']['all']
        issues = self.redmine.issue.all()
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(issues[0].subject, 'Foo')
        self.assertEqual(issues[1].id, 2)
        self.assertEqual(issues[1].subject, 'Bar')

    def test_issue_filter(self):
        self.response.json.return_value = responses['issue']['filter']
        issues = self.redmine.issue.filter(project_id=1)
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(issues[0].subject, 'Foo')
        self.assertEqual(issues[1].id, 2)
        self.assertEqual(issues[1].subject, 'Bar')

    def test_issue_relations(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.assertIsInstance(issue.relations, ResourceSet)
        self.assertIsInstance(issue.time_entries, ResourceSet)

    def test_time_entry_version(self):
        self.assertEqual(self.redmine.time_entry.resource_class.version, '1.1')

    def test_time_entry_get(self):
        self.response.json.return_value = responses['time_entry']['get']
        time_entry = self.redmine.time_entry.get(1)
        self.assertEqual(time_entry.id, 1)
        self.assertEqual(time_entry.hours, 2)

    def test_time_entry_all(self):
        self.response.json.return_value = responses['time_entry']['all']
        time_entries = self.redmine.time_entry.all()
        self.assertEqual(time_entries[0].id, 1)
        self.assertEqual(time_entries[0].hours, 3)
        self.assertEqual(time_entries[1].id, 2)
        self.assertEqual(time_entries[1].hours, 4)

    def test_time_entry_filter(self):
        self.response.json.return_value = responses['time_entry']['filter']
        time_entries = self.redmine.time_entry.filter(issue_id=1)
        self.assertEqual(time_entries[0].id, 1)
        self.assertEqual(time_entries[0].hours, 3)
        self.assertEqual(time_entries[1].id, 2)
        self.assertEqual(time_entries[1].hours, 4)

    def test_enumeration_version(self):
        self.assertEqual(self.redmine.enumeration.resource_class.version, '2.2')

    def test_enumeration_filter(self):
        self.response.json.return_value = responses['enumeration']['filter']
        enumerations = self.redmine.enumeration.filter(resource='time_entry_activities')
        self.assertEqual(enumerations[0].id, 1)
        self.assertEqual(enumerations[0].name, 'Foo')
        self.assertEqual(enumerations[1].id, 2)
        self.assertEqual(enumerations[1].name, 'Bar')

    def test_attachment_version(self):
        self.assertEqual(self.redmine.attachment.resource_class.version, '1.3')

    def test_attachment_get(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        self.assertEqual(attachment.id, 1)
        self.assertEqual(attachment.filename, 'foo.jpg')

    def test_wiki_page_version(self):
        self.assertEqual(self.redmine.wiki_page.resource_class.version, '2.2')

    def test_wiki_page_get(self):
        self.response.json.return_value = responses['wiki_page']['get']
        wiki_page = self.redmine.wiki_page.get('title', project_id=1)
        self.assertEqual(wiki_page.title, 'Foo')

    def test_wiki_page_filter(self):
        self.response.json.return_value = responses['wiki_page']['filter']
        wiki_pages = self.redmine.wiki_page.filter(project_id=1)
        self.assertEqual(wiki_pages[0].title, 'Foo')
        self.assertEqual(wiki_pages[1].title, 'Bar')

    def test_project_membership_version(self):
        self.assertEqual(self.redmine.project_membership.resource_class.version, '1.4')

    def test_project_membership_get(self):
        self.response.json.return_value = responses['project_membership']['get']
        membership = self.redmine.project_membership.get(1)
        self.assertEqual(membership.id, 1)

    def test_project_membership_filter(self):
        self.response.json.return_value = responses['project_membership']['filter']
        memberships = self.redmine.project_membership.filter(project_id=1)
        self.assertEqual(memberships[0].id, 1)
        self.assertEqual(memberships[1].id, 2)

    def test_issue_category_version(self):
        self.assertEqual(self.redmine.issue_category.resource_class.version, '1.3')

    def test_issue_category_get(self):
        self.response.json.return_value = responses['issue_category']['get']
        issue_category = self.redmine.issue_category.get(1)
        self.assertEqual(issue_category.id, 1)
        self.assertEqual(issue_category.name, 'Foo')

    def test_issue_category_filter(self):
        self.response.json.return_value = responses['issue_category']['filter']
        categories = self.redmine.issue_category.filter(project_id=1)
        self.assertEqual(categories[0].id, 1)
        self.assertEqual(categories[0].name, 'Foo')
        self.assertEqual(categories[1].id, 2)
        self.assertEqual(categories[1].name, 'Bar')

    def test_issue_relation_version(self):
        self.assertEqual(self.redmine.issue_relation.resource_class.version, '1.3')

    def test_issue_relation_get(self):
        self.response.json.return_value = responses['issue_relation']['get']
        relation = self.redmine.issue_relation.get(1)
        self.assertEqual(relation.id, 1)

    def test_issue_relation_filter(self):
        self.response.json.return_value = responses['issue_relation']['filter']
        relations = self.redmine.issue_relation.filter(issue_id=1)
        self.assertEqual(relations[0].id, 1)
        self.assertEqual(relations[1].id, 2)

    def test_version_version(self):
        self.assertEqual(self.redmine.version.resource_class.version, '1.3')

    def test_version_get(self):
        self.response.json.return_value = responses['version']['get']
        version = self.redmine.version.get(1)
        self.assertEqual(version.id, 1)
        self.assertEqual(version.name, 'Foo')

    def test_version_filter(self):
        self.response.json.return_value = responses['version']['filter']
        versions = self.redmine.version.filter(project_id=1)
        self.assertEqual(versions[0].id, 1)
        self.assertEqual(versions[0].name, 'Foo')
        self.assertEqual(versions[1].id, 2)
        self.assertEqual(versions[1].name, 'Bar')

    def test_user_version(self):
        self.assertEqual(self.redmine.user.resource_class.version, '1.1')

    def test_user_get(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get(1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.firstname, 'John')

    def test_user_all(self):
        self.response.json.return_value = responses['user']['all']
        users = self.redmine.user.all()
        self.assertEqual(users[0].id, 1)
        self.assertEqual(users[0].firstname, 'John')
        self.assertEqual(users[1].id, 2)
        self.assertEqual(users[1].firstname, 'Jack')

    def test_user_filter(self):
        self.response.json.return_value = responses['user']['filter']
        users = self.redmine.user.filter(status_id=2)
        self.assertEqual(users[0].id, 1)
        self.assertEqual(users[0].firstname, 'John')
        self.assertEqual(users[1].id, 2)
        self.assertEqual(users[1].firstname, 'Jack')

    def test_group_version(self):
        self.assertEqual(self.redmine.group.resource_class.version, '2.1')

    def test_group_get(self):
        self.response.json.return_value = responses['group']['get']
        group = self.redmine.group.get(1)
        self.assertEqual(group.id, 1)
        self.assertEqual(group.name, 'Foo')

    def test_group_all(self):
        self.response.json.return_value = responses['group']['all']
        groups = self.redmine.group.all()
        self.assertEqual(groups[0].id, 1)
        self.assertEqual(groups[0].name, 'Foo')
        self.assertEqual(groups[1].id, 2)
        self.assertEqual(groups[1].name, 'Bar')

    def test_role_version(self):
        self.assertEqual(self.redmine.role.resource_class.version, '1.4')

    def test_role_get(self):
        self.response.json.return_value = responses['role']['get']
        role = self.redmine.role.get(1)
        self.assertEqual(role.id, 1)
        self.assertEqual(role.name, 'Foo')

    def test_role_all(self):
        self.response.json.return_value = responses['role']['all']
        roles = self.redmine.role.all()
        self.assertEqual(roles[0].id, 1)
        self.assertEqual(roles[0].name, 'Foo')
        self.assertEqual(roles[1].id, 2)
        self.assertEqual(roles[1].name, 'Bar')

    def test_news_version(self):
        self.assertEqual(self.redmine.news.resource_class.version, '1.1')

    def test_news_all(self):
        self.response.json.return_value = responses['news']['all']
        news = self.redmine.news.all()
        self.assertEqual(news[0].id, 1)
        self.assertEqual(news[0].title, 'Foo')
        self.assertEqual(news[1].id, 2)
        self.assertEqual(news[1].title, 'Bar')

    def test_news_filter(self):
        self.response.json.return_value = responses['news']['filter']
        news = self.redmine.news.filter(project_id=1)
        self.assertEqual(news[0].id, 1)
        self.assertEqual(news[0].title, 'Foo')
        self.assertEqual(news[1].id, 2)
        self.assertEqual(news[1].title, 'Bar')

    def test_issue_status_version(self):
        self.assertEqual(self.redmine.issue_status.resource_class.version, '1.3')

    def test_issue_status_all(self):
        self.response.json.return_value = responses['issue_status']['all']
        statuses = self.redmine.issue_status.all()
        self.assertEqual(statuses[0].id, 1)
        self.assertEqual(statuses[0].name, 'Foo')
        self.assertEqual(statuses[1].id, 2)
        self.assertEqual(statuses[1].name, 'Bar')

    def test_tracker_version(self):
        self.assertEqual(self.redmine.tracker.resource_class.version, '1.3')

    def test_tracker_all(self):
        self.response.json.return_value = responses['tracker']['all']
        trackers = self.redmine.tracker.all()
        self.assertEqual(trackers[0].id, 1)
        self.assertEqual(trackers[0].name, 'Foo')
        self.assertEqual(trackers[1].id, 2)
        self.assertEqual(trackers[1].name, 'Bar')

    def test_query_version(self):
        self.assertEqual(self.redmine.query.resource_class.version, '1.3')

    def test_query_all(self):
        self.response.json.return_value = responses['query']['all']
        queries = self.redmine.query.all()
        self.assertEqual(queries[0].id, 1)
        self.assertEqual(queries[0].name, 'Foo')
        self.assertEqual(queries[1].id, 2)
        self.assertEqual(queries[1].name, 'Bar')

    def test_custom_field_version(self):
        self.assertEqual(self.redmine.custom_field.resource_class.version, '2.4')

    def test_custom_field_all(self):
        self.response.json.return_value = responses['custom_field']['all']
        fields = self.redmine.custom_field.all()
        self.assertEqual(fields[0].id, 1)
        self.assertEqual(fields[0].name, 'Foo')
        self.assertEqual(fields[1].id, 2)
        self.assertEqual(fields[1].name, 'Bar')
