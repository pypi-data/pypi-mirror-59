from chisubmit.backend.api.models import Course
from chisubmit.tests.integration.clientlibs import ChisubmitClientLibsTestCase
from chisubmit.tests.common import COURSE1_USERS, COURSE2_USERS
from chisubmit.client.exceptions import UnknownObjectException,\
    BadRequestException

class CourseTests(ChisubmitClientLibsTestCase):
    
    fixtures = ['users', 'course1']
    
    def test_get_courses(self):
        c = self.get_api_client("admintoken")
        
        courses = c.get_courses()
        self.assertEqual(len(courses), 1)
    
    def test_get_course(self):
        c = self.get_api_client("admintoken")
        
        course = c.get_course("cmsc40100")
        self.assertEqual(course.name, "Introduction to Software Testing")
        

    def test_create_course(self):
        c = self.get_api_client("admintoken")
        
        course = c.create_course(course_id = "cmsc40110",
                                 name = "Advanced Software Testing")
        self.assertEqual(course.name, "Advanced Software Testing")
        
        try:
            course_obj = Course.objects.get(course_id="cmsc40110")
        except Course.DoesNotExist:
            self.fail("Course was not added to database")  
            
        self.assertEqual(course_obj.course_id, "cmsc40110")
        self.assertEqual(course_obj.name, "Advanced Software Testing")
        
        
    def test_edit_course_1(self):
        c = self.get_api_client("admintoken")
        
        course = c.get_course("cmsc40100")
        
        course.edit(name="Intro to Software Testing",
                    default_extensions = 10)

        self.assertEqual(course.name, "Intro to Software Testing")
        self.assertEqual(course.default_extensions, 10)
                 
        try:
            course_obj = Course.objects.get(course_id="cmsc40100")
        except Course.DoesNotExist:
            self.fail("Course not found in database")  
            
        self.assertEqual(course_obj.name, "Intro to Software Testing")
        self.assertEqual(course_obj.default_extensions, 10)
        
    def test_edit_course_2(self):
        c = self.get_api_client("admintoken")
        
        course = c.get_course("cmsc40100")
        
        course.name = "Intro to Software Testing"
        course.default_extensions = 10

        self.assertEqual(course.name, "Intro to Software Testing")
        self.assertEqual(course.default_extensions, 10)
                 
        try:
            course_obj = Course.objects.get(course_id="cmsc40100")
        except Course.DoesNotExist:
            self.fail("Course not found in database")  
            
        self.assertEqual(course_obj.name, "Intro to Software Testing")
        self.assertEqual(course_obj.default_extensions, 10)
        
    def test_edit_course_3(self):
        c = self.get_api_client("admintoken", deferred_save = True)
        
        course = c.get_course("cmsc40100")
        
        course.name = "Intro to Software Testing"
        course.default_extensions = 10

        self.assertEqual(course.name, "Intro to Software Testing")
        self.assertEqual(course.default_extensions, 10)
                 
        try:
            course_obj = Course.objects.get(course_id="cmsc40100")
        except Course.DoesNotExist:
            self.fail("Course not found in database")  
            
        self.assertEqual(course_obj.name, "Introduction to Software Testing")
        self.assertEqual(course_obj.default_extensions, 0)
        
        course.save()                   
        
        try:
            course_obj = Course.objects.get(course_id="cmsc40100")
        except Course.DoesNotExist:
            self.fail("Course not found in database")  
            
        self.assertEqual(course.name, "Intro to Software Testing")
        self.assertEqual(course.default_extensions, 10)
        
                 
class CoursePermissionsTests(ChisubmitClientLibsTestCase):
    
    fixtures = ['users', 'course1', 'course1_users', 'course2', 'course2_users']
    
    def test_get_courses_admin(self):
        c = self.get_api_client("admintoken")
        
        courses = c.get_courses()
        self.assertEqual(len(courses), 2)
        
    def test_get_courses_course1(self):
        for user in COURSE1_USERS:
            c = self.get_api_client(user + "token")
            
            courses = c.get_courses()
            self.assertEqual(len(courses), 1)
            self.assertEqual(courses[0].name, "Introduction to Software Testing")
        
    def test_get_courses_course2(self):
        for user in COURSE2_USERS:
            c = self.get_api_client(user + "token")
            
            courses = c.get_courses()
            self.assertEqual(len(courses), 1)
            self.assertEqual(courses[0].name, "Advanced Software Testing")
        
    def test_get_course_course1(self):
        for user in COURSE1_USERS:
            c = self.get_api_client(user + "token")
            
            with self.assertRaises(UnknownObjectException):
                c.get_course("cmsc40110")    

    def test_get_course_course2(self):
        for user in COURSE2_USERS:
            c = self.get_api_client(user + "token")
            
            with self.assertRaises(UnknownObjectException):
                c.get_course("cmsc40100")  
        
              
class CourseValidationTests(ChisubmitClientLibsTestCase):
    
    fixtures = ['users', 'course1', 'course2']
    
    def test_create_course_invalid_id(self):
        c = self.get_api_client("admintoken")
        
        with self.assertRaises(BadRequestException) as cm:
            course = c.create_course(course_id = "cmsc 40200",
                                     name = "Advanced Validation Testing")
        
        bre = cm.exception
        self.assertCountEqual(list(bre.errors.keys()), ["course_id"])
        self.assertEqual(len(bre.errors["course_id"]), 1)
        
    def test_create_course_multiple_errors(self):
        c = self.get_api_client("admintoken")
        
        with self.assertRaises(BadRequestException) as cm:
            course = c.create_course(course_id = "cmsc 40210",
                                     name = None)
        
        bre = cm.exception
        self.assertCountEqual(list(bre.errors.keys()), ["course_id", "name"])
        self.assertEqual(len(bre.errors["course_id"]), 1)        
        self.assertEqual(len(bre.errors["name"]), 1)        
          
    def test_create_course_existing_course(self):
        c = self.get_api_client("admintoken")
        
        with self.assertRaises(BadRequestException) as cm:
            course = c.create_course(course_id = "cmsc40100",
                                     name = "Introduction to Software Testing")
        
        bre = cm.exception
        self.assertCountEqual(list(bre.errors.keys()), ["course_id"])
        self.assertEqual(len(bre.errors["course_id"]), 1)
        
class CourseArchivingTests(ChisubmitClientLibsTestCase):
    
    fixtures = ['users', 'course1', 'course2']
    
    def test_get_courses(self):
        c = self.get_api_client("admintoken")
        
        courses = c.get_courses()
        self.assertEqual(len(courses), 2)
        
        for c in courses:
            self.assertFalse(c.archived)
            
    def test_archive_course(self):
        c = self.get_api_client("admintoken")
        
        course = c.get_course("cmsc40110")
        course.archived = True
        
        try:
            course_obj = Course.objects.get(course_id="cmsc40110")
        except Course.DoesNotExist:
            self.fail("Course not found in database")  
            
        self.assertEqual(course_obj.archived, True)
        
        # Check that get_courses only returns the non-archived course
        courses = c.get_courses()
        self.assertEqual(len(courses), 1)
        
        course = courses[0]
        self.assertEqual(course.course_id, "cmsc40100")
        self.assertFalse(course.archived)
        
        # Check that we can still directly access the archived course
        course = c.get_course("cmsc40110")
        self.assertTrue(course.archived)
        
    def test_include_archived(self):     
        c = self.get_api_client("admintoken")
        
        courses = c.get_courses()   
        self.assertEqual(len(courses), 2)
        
        courses = c.get_courses(include_archived=True)   
        self.assertEqual(len(courses), 2)

        course = c.get_course("cmsc40110")
        course.archived = True
        
        courses = c.get_courses()   
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0].course_id, "cmsc40100")
        
        courses = c.get_courses(include_archived=True)   
        self.assertEqual(len(courses), 2)
        