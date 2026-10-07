from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.urls import reverse

from .models import Convocatoria


class ConvocatoriaTestCase(TestCase):
    def test_crear_convocatoria(self):
        convocatoria = Convocatoria.objects.create(
            titulo = "Curso de Python Avanzado",
            area = "Tecnología",
            descripcion = "Capacitación en desarrollo backend",
            fecha_inicio = "2026-10-01",
            fecha_final = "2026-10-15",
            ciudad = "Bogotá",
            cupos_totales = 30,
        )
        self.assertEqual(convocatoria.titulo, "Curso de Python Avanzado")
        self.assertEqual(convocatoria.cupos_asignados, 0)
        self.assertEqual(convocatoria.estado, "Borrador")
# Create your tests here.
#####################################################################################
#Prueba de Integracion 

from django.contrib.auth.models import User, Group

class ConvocatoriaIntegracionTestCase(TestCase):
    def setUp(self):
        self.grupo = Group.objects.create(name='Administradores')
        self.usuario_admin = User.objects.create_user(username='admin', password='admin123')
        self.usuario_admin.groups.add(self.grupo)
        self.client.login(username='admin', password='admin123')
        

    def test_crear_convocatoria_integracion(self):
        respuesta = self.client.get('/convocatorias/crear/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'app_convocatorias/app_convocatorias_form.html')
        datos_convocatoria = {
            'titulo': 'Curso Python Avanzado',
            'area': 'Tecnología',
            'descripcion': 'Capacitación en desarrollo backend',
            'fecha_inicio': '2026-10-01',
            'fecha_final': '2026-10-15',  # Nombre del campo según tu vista
            'ciudad': 'Bogotá',
            'cupos_totales': '30',
        }
        respuesta_post = self.client.post('/convocatorias/crear/', datos_convocatoria)
        self.assertEqual(Convocatoria.objects.count(), 1)
        convocatoria_creada = Convocatoria.objects.first()
        self.assertEqual(convocatoria_creada.titulo, 'Curso Python Avanzado')
        self.assertEqual(convocatoria_creada.area, 'Tecnología')

        self.assertEqual(convocatoria_creada.estado, 'Borrador')
        self.assertEqual(convocatoria_creada.cupos_asignados, 0)
        self.assertEqual(respuesta_post.status_code, 302)
        self.assertRedirects(respuesta_post, '/convocatorias/')
        respuesta_convocatorias = self.client.get('/convocatorias/')
        self.assertContains(respuesta_convocatorias, 'Curso Python Avanzado')

class ConvocatoriaOrdenIntegracionTestCase(TestCase):
    def setUp(self):
        self.grupo = Group.objects.create(name='Administradores')
        self.usuario_admin = User.objects.create_user(username='admin', password='admin123')
        self.usuario_admin.groups.add(self.grupo)
        self.client.login(username='admin', password='admin123')
        
        convocatoria = Convocatoria.objects.create(
            titulo = "C1",
            area = "Tecnología",
            descripcion = "Capacitación en desarrollo backend",
            fecha_inicio = "2026-11-01",
            fecha_final = "2026-11-08",
            ciudad = "Bogotá",
            cupos_totales = 30,
            estado = "Cerrada",
        )
                
        convocatoria2 = Convocatoria.objects.create(
            titulo = "C2",
            area = "Tecnología",
            descripcion = "Base de datos",
            fecha_inicio = "2026-09-20",
            fecha_final = "2026-09-28",
            ciudad = "Bogotá",
            cupos_totales = 30,
            
        )
        

        convocatoria3 = Convocatoria.objects.create(
            titulo = "C3",
            area = "Tecnología",
            descripcion = "desarrollo web",
            fecha_inicio = "2026-10-05",
            fecha_final = "2026-10-15",
            ciudad = "Bogotá",
            cupos_totales = 30,
            estado = "Publicada",
            
        )
                

    def test_listar_convocatoria_integracion(self):
        respuesta = self.client.get('/convocatorias/')
        self.assertEqual(respuesta.status_code, 200)
        convocatorias_en_contexto = respuesta.context['convocatorias']
        print(convocatorias_en_contexto)
        fechas_obtenidos = [convocatoria.fecha_inicio for convocatoria in convocatorias_en_contexto]
        fechas_esperados = sorted(fechas_obtenidos)
        self.assertEqual(fechas_obtenidos, fechas_esperados)
        
       
              
class ConsultarListadoConvocatorias(TestCase):
    def setUp(self):
        self.grupo = Group.objects.create(name='Administradores')
        self.usuario_admin = User.objects.create_user(username='admin', password='admin123')
        self.usuario_admin.groups.add(self.grupo)
        self.client.login(username='admin', password='admin123')
        '''datos_convocatoria = {
                        'titulo': 'Curso Python Avanzado',
                        'area': 'Tecnología',
                        'descripcion': 'Capacitación en desarrollo backend',
                        'fecha_inicio': '2026-10-01',
                        'fecha_final': '2026-10-15',  # Nombre del campo según tu vista
                        'ciudad': 'Bogotá',
                        'cupos_totales': '30',
                    }
            #Se envian los datos de la convocatoria mediante una solicitud POST a la ruta de creación de convocatorias.
            #Si los datos son válidos se almacenan en la base de datos
        respuesta_post = self.client.post('/convocatorias/crear/', datos_convocatoria)
        self.assertEqual(respuesta_post.status_code, 200)'''

    
    def test_consultar_nohay_convocatorias(self):
        respuesta_nohay = self.client.get('/convocatorias/')
        self.assertEqual(respuesta_nohay .status_code, 200)
        self.assertTemplateUsed(respuesta_nohay , 'app_convocatorias/app_convocatorias_gestionar.html') 
        self.assertContains(respuesta_nohay,'No hay resultados')            


class EditarConvocatoriaViewIntegracionTestCase(TestCase):
    def setUp(self):
        grupo = Group.objects.create(name='Administradores')
        usuario = User.objects.create_user(
            username='admin_edicion',
            password='admin123',
        )
        usuario.groups.add(grupo)
        self.client.login(username='admin_edicion', password='admin123')
        self.convocatoria = Convocatoria.objects.create(
            titulo='Curso de Python',
            area='Tecnología',
            descripcion='Capacitación inicial',
            fecha_inicio='2026-11-01',
            fecha_final='2026-11-10',
            ciudad='Bogotá',
            cupos_totales=10,
            cupos_asignados=3,
            estado=Convocatoria.Estado.PUBLICADA,
        )
        self.url = reverse(
            'app_convocatorias:detalle_convocatoria',
            args=[self.convocatoria.pk],
        )
        self.datos_actualizados = {
            'titulo': 'Curso de Python avanzado',
            'area': 'Desarrollo de software',
            'descripcion': 'Capacitación avanzada',
            'fecha_inicio': '2026-11-05',
            'fecha_final': '2026-11-15',
            'ciudad': 'Medellín',
            'cupos_totales': '8',
        }

    def test_get_muestra_formulario_edicion_con_datos_actuales(self):
        respuesta = self.client.get(self.url)

        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(
            respuesta,
            'app_convocatorias/app_convocatorias_form.html',
        )
        self.assertEqual(respuesta.context['modo'], 'Editar')
        self.assertEqual(
            respuesta.context['datos']['titulo'],
            self.convocatoria.titulo,
        )
        self.assertEqual(
            respuesta.context['datos']['fecha_inicio'],
            '2026-11-01',
        )
        self.assertContains(respuesta, 'Guardar convocatoria')

    def test_post_valido_actualiza_convocatoria_y_redirige_al_listado(self):
        respuesta = self.client.post(self.url, self.datos_actualizados)

        self.assertRedirects(
            respuesta,
            reverse('app_convocatorias:gestionar_convocatorias'),
        )
        self.convocatoria.refresh_from_db()
        self.assertEqual(self.convocatoria.titulo, 'Curso de Python avanzado')
        self.assertEqual(self.convocatoria.area, 'Desarrollo de software')
        self.assertEqual(self.convocatoria.descripcion, 'Capacitación avanzada')
        self.assertEqual(self.convocatoria.fecha_inicio.isoformat(), '2026-11-05')
        self.assertEqual(self.convocatoria.fecha_final.isoformat(), '2026-11-15')
        self.assertEqual(self.convocatoria.ciudad, 'Medellín')
        self.assertEqual(self.convocatoria.cupos_totales, 8)
        self.assertEqual(self.convocatoria.cupos_asignados, 3)
        self.assertEqual(
            self.convocatoria.estado,
            Convocatoria.Estado.PUBLICADA,
        )

    def test_post_no_permite_reducir_cupos_bajo_los_asignados(self):
        datos_invalidos = {
            **self.datos_actualizados,
            'cupos_totales': '2',
        }

        respuesta = self.client.post(self.url, datos_invalidos)

        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(
            respuesta,
            'app_convocatorias/app_convocatorias_form.html',
        )
        self.assertIn(
            'cupos_totales',
            respuesta.context['errores'],
        )
        self.convocatoria.refresh_from_db()
        self.assertEqual(self.convocatoria.titulo, 'Curso de Python')
        self.assertEqual(self.convocatoria.cupos_totales, 10)
               